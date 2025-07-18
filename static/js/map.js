fetch('/api/trips')
  .then(r => r.json())
  .then(trips => {
    const map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OSM'
    }).addTo(map);

    trips.forEach(t => {
      const marker = L.marker([t.lat, t.lng]).addTo(map);
      let popup = `<strong>${t.title}</strong><br>${t.location}<br>${t.start} → ${t.end}`;
      if (t.photos.length) {
        popup += '<br><div class="popup-photos">';
        t.photos.forEach(p => {
          popup += `<img src="/static/uploads/${p.filename}" style="width:120px;margin:2px">`;
        });
        popup += '</div>';
      }
      marker.bindPopup(popup);
    });
  });