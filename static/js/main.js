document.addEventListener('DOMContentLoaded', () => {
  const locationBtn = document.getElementById('locationBtn');
  const locationStatus = document.getElementById('locationStatus');

  if (locationBtn && locationStatus) {
    locationBtn.addEventListener('click', () => {
      if (!navigator.geolocation) {
        locationStatus.textContent = 'Geolocation is not supported by this browser.';
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;
          const mapLink = `https://www.google.com/maps?q=${latitude},${longitude}`;
          locationStatus.innerHTML = `Latitude: ${latitude.toFixed(5)}<br>Longitude: ${longitude.toFixed(5)}<br><a href="${mapLink}" target="_blank">Open in map</a>`;
        },
        () => {
          locationStatus.textContent = 'Location permission was denied or unavailable.';
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    });
  }
});
