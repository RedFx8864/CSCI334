function refreshDashboard() {

    fetch("/dashboard-data/")

    .then(response => response.json())

    .then(data => {

        document.getElementById(
            "total"
        ).innerText = data.total


        document.getElementById(
            "available"
        ).innerText = data.available


        document.getElementById(
            "occupied"
        ).innerText = data.occupied


        document.getElementById(
            "lastUpdated"
        ).innerText = data.last_updated


        document
        .querySelectorAll(".spot")

        .forEach(spot => {

            const spotId = parseInt(
                spot.dataset.spotId
            )


            if (
                data.occupied_spot_ids
                .includes(spotId)
            ) {

                spot.classList.remove(
                    "available"
                )

                spot.classList.add(
                    "occupied"
                )

                spot.innerHTML =
                    "Spot "
                    + spotId +
                    "<br>Occupied"

            }

            else {

                spot.classList.remove(
                    "occupied"
                )

                spot.classList.add(
                    "available"
                )

                spot.innerHTML =
                    "Spot "
                    + spotId +
                    "<br>Available"

            }

        })

    })

}

refreshDashboard()

setInterval(
    refreshDashboard,
    3000
)