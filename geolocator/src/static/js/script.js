document.getElementById("get-location").addEventListener("click", () => {
    if ("geolocation" in navigator) {
        // Request geolocation permission
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // User granted permission
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Send geolocation to the server
                fetch("/get-geolocation", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ latitude, longitude }),
                })
                .then(response => response.json())
                .then(data => {
                    // Display the result in a styled format
                    const messageDiv = document.getElementById("message");
                    messageDiv.innerHTML = `
                        <div class="custom-card">
                            <p class="text-sm text-gray-600">Latitude</p>
                            <p class="font-semibold">${data.latitude}</p>
                        </div>
                        <div class="custom-card">
                            <p class="text-sm text-gray-600">Longitude</p>
                            <p class="font-semibold">${data.longitude}</p>
                        </div>
                        <div class="custom-card">
                            <p class="text-sm text-gray-600">Place</p>
                            <p class="font-semibold">${data.place_name}</p>
                        </div>
                    `;
                })
                .catch(error => {
                    document.getElementById("message").innerHTML = `
                        <div class="bg-red-50 p-4 rounded-lg text-red-600">
                            Error sending location to the server.
                        </div>
                    `;
                });
            },
            (error) => {
                // User denied permission or an error occurred
                document.getElementById("message").innerHTML = `
                    <div class="bg-red-50 p-4 rounded-lg text-red-600">
                        Permission denied or unable to retrieve location.
                    </div>
                `;
            }
        );
    } else {
        document.getElementById("message").innerHTML = `
            <div class="bg-red-50 p-4 rounded-lg text-red-600">
                Geolocation is not supported by your browser.
            </div>
        `;
    }
});