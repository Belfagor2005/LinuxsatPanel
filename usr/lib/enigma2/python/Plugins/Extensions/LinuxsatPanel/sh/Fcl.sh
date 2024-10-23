#!/bin/sh
[ -d /tmp/xtest ] || mkdir -p /tmp/xtest
cd /tmp/xtest
####################################################################################################
####################################################################################################
echo "Downloading:"
####################################################################################################

####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -s -k -Lbk -A -k -m 8 -m 52    http://dream4evertwo.info/index.php?pages/D4E/ > /tmp/xtest/CCcam


sed -ne 's#.*HOST:\([^/]*\).*#\1#p' CCcam > adresa
sed -ne 's#.*">\([^/]*\).*#\1#p' adresa > adresa1
sed -i 's/<//' adresa1
sed -i 's/-.*//' adresa1

sed -ne 's#.*PORT:.*>\(.*\)</span></strong>.*#\1#p' CCcam > port
cat port | tr -dc '0-9\n' > port1                       # take numbers only (from whole string)

sed -ne 's#.*USER:\([^/]*\).*#\1#p' CCcam > user
sed -ne 's#.*">\([^/]*\).*#\1#p' user > user1
sed -i 's/<//' user1
#sed -i 's/remove the star//' user1
#sed -i 's/-//' user1
#sed -i 's/*//' user1

sed -ne 's#.*PASS:\([^/]*\).*#\1#p' CCcam > pass
sed -ne 's#.*">\([^/]*\).*#\1#p' pass > pass1
sed -i 's/<//' pass1

echo "C: "  > hotovo
sed -n '1,1p' adresa1 >> hotovo
echo -n " "  >> hotovo
sed -n '1,1p' port1 >> hotovo
echo -n " "  >> hotovo
sed -n '1,1p' user1 >> hotovo
echo -n " "  >> hotovo
sed -n '1,1p' pass1 >> hotovo
sed -n 'H; $x; $s/\n//gp' hotovo > hotovo1
echo "C: "  > hotovo
sed -n '2,2p' adresa1 >> hotovo
echo -n " "  >> hotovo
sed -n '2,2p' port1 >> hotovo
echo -n " "  >> hotovo
sed -n '2,2p' user1 >> hotovo
echo -n " "  >> hotovo
sed -n '2,2p' pass1 >> hotovo
sed -n 'H; $x; $s/\n//gp' hotovo > hotovo2
echo "C: "  > hotovo
sed -n '3,3p' adresa1 >> hotovo
echo -n " "  >> hotovo
sed -n '3,3p' port1 >> hotovo
echo -n " "  >> hotovo
sed -n '3,3p' user1 >> hotovo
echo -n " "  >> hotovo
sed -n '3,3p' pass1 >> hotovo
sed -n 'H; $x; $s/\n//gp' hotovo > hotovo3

cat hotovo1 hotovo2 hotovo3 > ok
sed -i 's/    / /' ok
sed -i 's/*//' ok

grep -o -i -E 'C: [a-z][^<]*' ok  >> /etc/CCcam.cfg
grep -o -i -E 'C: [a-z][^<]*' ok  > /tmp/xtest/soubor4

more /tmp/xtest/soubor4
####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -k -A -k -s  https://yalasat.com/%D8%B3%D9%8A%D8%B1%D9%81%D8%B1-%D8%B3%D9%8A%D8%B3%D9%83%D8%A7%D9%85-%D8%A7%D9%84%D9%85%D8%AC%D8%A7%D9%86%D9%8A-%D8%A7%D9%84%D9%85%D9%82%D8%AF%D9%85-%D9%85%D9%86-%D9%81%D8%B1%D9%8A%D9%82-store-sat/ > /tmp/xtest/CCcam
grep  -o -i -E 'HOST/URL.*?>(.*?)<[^<]*' CCcam > /tmp/xtest/CCcam1
grep -oE 'center;"><strong>[^<]*|text-align: center;"><b>[^<]*' CCcam1 | grep -oE '[^>]*$' | sed 's/  */ /g' > /tmp/xtest/CCcam2
sed 'N;N;N;s/\n/ /g' /tmp/xtest/CCcam2 | sed '1s/^/C: /'  > /tmp/xtest/CCcam
grep -o -i -E 'C: [a-z][^<]*' CCcam  >> /etc/CCcam.cfg
grep -o -i -E 'C: [a-z][^<]*' CCcam  > /tmp/xtest/soubor5

more /tmp/xtest/soubor5
####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -Lbk -m 4555 -m 6555 -k -s  https://skyhd.xyz/freetest/CCcam.cfg > /tmp/xtest/CCcam
grep -o -i -E '.*Expire' CCcam | sed "s#Expire##g"  >> /etc/CCcam.cfg
grep -o -i -E '.*Expire' CCcam | sed "s#Expire##g"  > /tmp/xtest/soubor6

more /tmp/xtest/soubor6
####################################################################################################

####################################################################################################
KINGHD="https://kinghd.info/cccamtest3d.php"
curl --max-time 5.5 --speed-time 9 --speed-limit 10 --max-time 4 --connect-timeout 4  --limit-rate 50K  -Lbk -m 4555 -m 6555 -k  -s  "$KINGHD" > /tmp/xtest/a
sed -ne 's#.*Username"  value="\([^"]*\).*#\1#p' /tmp/xtest/a > /tmp/xtest/name
sed -ne 's#.*Password"  value="\([^"]*\).*#\1#p' /tmp/xtest/a > /tmp/xtest/pass
PATH_J_XM=$(cat /tmp/xtest/name 2>/dev/null &)
PATH_J_XM2=$(cat /tmp/xtest/pass 2>/dev/null &)

curl --max-time 5.5 --limit-rate 50K -Lbk -m 4555 -m 6555 -k -s 'https://kinghd.info/cccamtest3d.php' \
--compressed \
-X POST \
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
-H 'Accept-Language: cs,sk;q=0.8,en-US;q=0.5,en;q=0.3' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: https://kinghd.info' \
-H 'Connection: keep-alive' \
-H 'Referer: https://kinghd.info/cccamtest3d.php' \
-H 'Cookie: _ga_WLWQ1BK3KQ=GS1.1.1716017670.3.1.1716017682.0.0.0; _ga=GA1.1.758573741.1707053530' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'Sec-Fetch-Dest: document' \
-H 'Sec-Fetch-Mode: navigate' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Sec-Fetch-User: ?1' \
--data-raw 'umarcccam2server=umarcccam2server&Username='"$PATH_J_XM"'&Password='"$PATH_J_XM2"'' \
> /tmp/xtest/CCcam

grep -o -i -E 'C: [a-z][^<]*' CCcam | sed -n '2p'  > /tmp/xtest/soubor9

more /tmp/xtest/soubor9

####################################################################################################
KINGHD="https://kinghd.info/cccamtest2d.php"
curl --max-time 5.5 --speed-time 9 --speed-limit 10 --max-time 4 --connect-timeout 4  --limit-rate 50K  -Lbk -m 4555 -m 6555 -k  -s  "$KINGHD" > /tmp/xtest/a
sed -ne 's#.*Username"  value="\([^"]*\).*#\1#p' /tmp/xtest/a > /tmp/xtest/name
sed -ne 's#.*Password"  value="\([^"]*\).*#\1#p' /tmp/xtest/a > /tmp/xtest/pass
PATH_J_XM=$(cat /tmp/xtest/name 2>/dev/null &)
PATH_J_XM2=$(cat /tmp/xtest/pass 2>/dev/null &)

curl --max-time 5.5 --limit-rate 50K -Lbk -m 4555 -m 6555 -k -s 'https://kinghd.info/cccamtest2d.php' \
--compressed \
-X POST \
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
-H 'Accept-Language: cs,sk;q=0.8,en-US;q=0.5,en;q=0.3' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: https://kinghd.info' \
-H 'Connection: keep-alive' \
-H 'Referer: https://kinghd.info/cccamtest2d.php' \
-H 'Cookie: _ga_WLWQ1BK3KQ=GS1.1.1716017670.3.1.1716018247.0.0.0; _ga=GA1.1.758573741.1707053530' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'Sec-Fetch-Dest: document' \
-H 'Sec-Fetch-Mode: navigate' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Sec-Fetch-User: ?1' \
--data-raw 'Username='"$PATH_J_XM"'&Password='"$PATH_J_XM2"'&expireshow=&cccamtest%40kinghd%401122=' \
> /tmp/xtest/CCcam

grep -o -i -E 'C: [a-z][^<]*' CCcam | sed -n '2p'  > /tmp/xtest/soubor10

more /tmp/xtest/soubor10
####################################################################################################
curl --max-time 52 --limit-rate 100K -L -s "https://drive.usercontent.google.com/u/0/uc?id=1_8qWPKM6pc4q9Q1YUEN0fiqur9XvoZpR&export=download" > /tmp/xtest/CCcam
grep -o -i -E 'C: [a-z][^<]*' /tmp/xtest/CCcam > /tmp/xtest/soubor11
more /tmp/xtest/soubor11
####################################################################################################
generate_random_letters() {
    tr -dc 'a-z' < /dev/urandom | dd bs=3 count=1 2>/dev/null
}


username=$(generate_random_letters 2>/dev/null)
password=$(generate_random_letters 2>/dev/null)



echo "Username: $username" >/dev/null 2>&1
echo "Password: $password" >/dev/null 2>&1

curl --max-time 5.5  -k -A -k -s 'http://www.clinehub.com/freetest/' --compressed -X POST \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' \
  -H 'Accept-Language: cs,sk;q=0.8,en-US;q=0.5,en;q=0.3' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: http://www.clinehub.com' \
  -H 'Connection: keep-alive' \
  -H 'Referer: http://www.clinehub.com/freetest/' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'Priority: u=0, i' \
  --data-raw '2freecccamKinhdUMARALI2=2freecccamKinhdUMARALI2&Username='"$username"$'&Password='"$password"$'' \
  > /tmp/xtest/CCcam
  
grep -o -i -E 'C: [a-z][^<]*' CCcam | sed -n '2p'  > /tmp/xtest/soubor12

more /tmp/xtest/soubor12
####################################################################################################
####################################################################################################
####################################################################################################
curl  --limit-rate 100K  -k -Lbk -A -k -m 8000 -m 5200 -s  https://cccamsate.com/free > /tmp/xtest/CCcam

grep -o -i -E 'C: [a-z][^<]*' CCcam  > /tmp/xtest/soubor14

more /tmp/xtest/soubor14
####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -s -k -Lbk -A -k -m 8 -m 52  https://cccamia.com/free-cccam/ > /tmp/xtest/CCcam 

grep -o -i -E 'C: [a-z][^<]*' CCcam  > /tmp/xtest/soubor15

more /tmp/xtest/soubor15
####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -s -k -Lbk -A -k -m 8 -m 52  https://cccamhub.com/cccamfree/ > /tmp/xtest/CCcam

grep -o -i 'C: free[^<]*' CCcam  > /tmp/xtest/soubor16

more /tmp/xtest/soubor16
####################################################################################################
curl --max-time 5.5  --limit-rate 100K     -s -k -Lbk -A -k -m 8 -m 52  https://cccamiptv.club/free-cccam/#page-content > /tmp/xtest/CCcam

grep -o -i 'C: free[^<]*' CCcam > /tmp/xtest/soubor17

more /tmp/xtest/soubor17
####################################################################################################
####################################################################################################
####################################################################################################

cat soubor{1..28} > /tmp/CCcam.cfg 2>/dev/null || true
sed -i "s/c:/C:/" /tmp/CCcam.cfg
while read radek; do
    pocet=$(echo $radek | wc -w)
    if [ $pocet -gt 4 ]; then
        echo $radek >> /tmp/CCcam.cfg2
    fi
done < '/tmp/CCcam.cfg'
cd /
rm -rf /etc/CCcam.cfg
cp /tmp/CCcam.cfg2 /etc/CCcam.cfg
rm -rf /tmp/CCcam.cfg2
rm -rf /tmp/CCcam.cfg
rm -rf /tmp/xtest
rm -rf /CCcam*
rm -rf /hotovo*
more /etc/CCcam.cfg
cat /etc/CCcam.cfg > /tmp/CCcam.cfg
echo "Applying -DATAx..."
cat /etc/CCcamDATAx.cfg > /etc/CCcam.cfg
echo "" >> /etc/CCcam.cfg
grep -v '^ *$' /tmp/CCcam.cfg >> /etc/CCcam.cfg
sed -i "/^$/d " /etc/CCcam.cfg
rm -rf /tmp/CCcam.cfg
sleep 0
OUTPUT2='/tmp/server'
echo ""
echo -n "Converting ....."
FS=" "
group_number=1
cat /etc/CCcam.cfg | grep -i "^C:.*" | while read line ; do
    SERVER=$(echo $line | cut -d"$FS" -f2)
    PORT=$(echo $line | cut -d"$FS" -f3)
    USER=$(echo $line | cut -d"$FS" -f4)
    PASS=$(echo $line | cut -d"$FS" -f5)

    echo -n "."

    echo "[reader]" >> $OUTPUT2
    echo "label = $SERVER" >> $OUTPUT2
    echo "protocol = cccam" >> $OUTPUT2
    echo "device = $SERVER,$PORT" >> $OUTPUT2
    echo "user = $USER" >> $OUTPUT2
    echo "password = $PASS" >> $OUTPUT2
    echo "ccckeepalive = 1" >> $OUTPUT2
    echo "inactivitytimeout = 30" >> $OUTPUT2
    echo "reconnecttimeout = 5" >> $OUTPUT2
    echo "disablecrccws = 1" >> $OUTPUT2
    echo "group = 1" >> $OUTPUT2
    echo "" >> $OUTPUT2
    echo "" >> $OUTPUT2


    #group_number=$((group_number+1))
done

cat /etc/OscamDATAx.cfg >> /tmp/server
sleep 0
cp /tmp/server /etc/tuxbox/config/oscam/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/oscam-emu/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/oscam_atv_free/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /var/tuxbox/config/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/gcam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/ncam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/supcam-emu/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/oscamicam/oscam.server  2>/dev/null || true
sleep 0
cp /tmp/server /etc/tuxbox/config/oscamicamnew/oscam.server  2>/dev/null || true
sleep 0

wait

rm -rf /tmp/server

cat /etc/CCcam.cfg > /etc/oscam.cfg

wait
echo ""
####################################################################################################
/etc/init.d/softcam restart
####################################################################################################
wait
pocet1=$(wc -l < /etc/CCcam.cfg)
pocet1=$pocet1
echo ""
echo "SERVERS..... "$pocet1
/tmp/upozor.sh >> /dev/null 2>&1 </dev/null &
rm -rf /tmp/upozor.sh >> /dev/null 2>&1 </dev/null &
rm -rf /tmp/cccam
rm -rf /tmp/cccam1

sleep 5

exit -0

