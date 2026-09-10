document.addEventListener('DOMContentLoaded', () => {
  const activateButton = document.getElementById('activateEmergencyBtn');
  const locationMessage = document.getElementById('locationMessage');

  if (!activateButton) return;

  activateButton.addEventListener('click', () => {
    if (!navigator.geolocation) {
      locationMessage.textContent = 'Location services are not available in this browser.';
      locationMessage.classList.remove('hidden');
      locationMessage.classList.add('alert-box');
      return;
    }

    locationMessage.textContent = 'Requesting your location...';
    locationMessage.classList.remove('hidden');
    locationMessage.classList.add('alert-box');

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const payload = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          risk_level: 'HIGH',
          symptoms: 'Emergency activated via dashboard'
        };

        try {
          const response = await fetch('/api/emergency/activate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          const data = await response.json();

          if (!response.ok) {
            locationMessage.textContent = data.error || 'Emergency activation failed.';
            locationMessage.classList.add('alert-box');
            return;
          }

          locationMessage.innerHTML = `
            <strong>Emergency assistance request created.</strong><br>
            Request ID: ${data.request_id}<br>
            Status: ${data.status}<br>
            Contacts notified: ${data.contacts_notified}<br>
            <a href="${data.map_link}" target="_blank">Open location</a>
          `;
          locationMessage.classList.add('success-box');
          locationMessage.classList.remove('alert-box');
          window.location.href = '/dashboard';
        } catch (error) {
          locationMessage.textContent = 'There was an error sending the emergency request.';
          locationMessage.classList.add('alert-box');
        }
      },
      () => {
        locationMessage.textContent = 'Location permission was denied. Please allow browser access to use emergency location sharing.';
        locationMessage.classList.add('alert-box');
      },
      { enableHighAccuracy: true, timeout: 15000 }
    );
  });
});
