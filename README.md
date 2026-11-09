# Elpriser SE3 per timme

Statisk sida (GitHub Pages) med timpriser för elområde SE3, senaste dagen överst.
`index.html` läser `data.json` (`{"YYYY-MM-DD":[öre/kWh per timme, ...]}`), ritar ett stapeldiagram per dag
(grönt/gult/rött efter tredjedelar av dagens spann) och en tabell med ungefärlig kostnad för vanliga sysslor
vid dagens billigaste och dyraste timme. Spotpris exkl. moms, energiskatt och nätavgift. Källa: elprisetjustnu.se.

## Daglig uppdatering
    python3 /workspace/elpriser/add_day.py YYYY-MM-DD

Hämtar dagens kvartspriser med `curl -A Mozilla`, räknar timsnitt i öre/kWh, lägger till dagen i `data.json`
(tidigare dagar ligger kvar), committar och pushar. Finns dagen redan händer inget (`--force` hämtar om den).
Lägg till `--no-push` för att testa lokalt.
