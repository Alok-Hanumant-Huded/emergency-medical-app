document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('emergencyForm');
  const locationMessage = document.getElementById('locationMessage');
  const activateButton = document.getElementById('activateEmergencyBtn');

  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const riskLevel = document.getElementById('riskLevel').value;
    const symptoms = document.getElementById('symptoms').value.trim();

    if (!riskLevel || !symptoms) {
      locationMessage.textContent =
        'Please select the risk level and enter your symptoms.';
      locationMessage.classList.remove('hidden');
      return;
    }

    if (!navigator.geolocation) {
      locationMessage.textContent =
        'Location services are not available in this browser.';
      locationMessage.classList.remove('hidden');
      return;
    }

    activateButton.disabled = true;
    activateButton.textContent = 'GETTING LOCATION...';

    locationMessage.textContent = 'Requesting your location...';
    locationMessage.classList.remove('hidden');

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const payload = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          risk_level: riskLevel,
          symptoms: symptoms
        };

        try {
          const response = await fetch('/api/emergency/activate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          });

          const data = await response.json();

          if (!response.ok) {
            throw new Error(data.error || 'Emergency activation failed.');
          }

          locationMessage.innerHTML = `
            <strong>🚑 Emergency assistance request created.</strong><br>
            Request ID: ${data.request_id}<br>
            Status: ${data.status}<br>
            Contacts notified: ${data.contacts_notified}<br>
            <a href="${data.map_link}" target="_blank">Open location</a>
          `;

          locationMessage.classList.add('success-box');
          locationMessage.classList.remove('alert-box');

          setTimeout(() => {
            window.location.href = '/dashboard';
          }, 2000);

        } catch (error) {
          locationMessage.textContent = error.message;
          locationMessage.classList.add('alert-box');
          activateButton.disabled = false;
          activateButton.textContent = '🚨 ACTIVATE EMERGENCY';
        }
      },
      () => {
        locationMessage.textContent =
          'Location permission was denied. Please allow location access in your browser.';
        locationMessage.classList.add('alert-box');
        activateButton.disabled = false;
        activateButton.textContent = '🚨 ACTIVATE EMERGENCY';
      },
      {
        enableHighAccuracy: true,
        timeout: 15000
      }
    );
  });
});
