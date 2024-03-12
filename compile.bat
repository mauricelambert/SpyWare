python -m zipapp SpyWare -c -p "/usr/bin/env python3"
move SpyWare.pyz bin/SpyWare.pyz

python bin/SpyWare.pyz -r --install --env "screenSpy.conf=abc.conf" --enable runonly -s abc.conf
