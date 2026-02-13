#!/system/bin/sh
OUTPUT2="/var/bin/sharkn/ncam.server"
rm $OUTPUT2 > /dev/null 2>&1

LIST_URL="https://raw.githubusercontent.com/Badr-cx/icone-wegoo/refs/heads/main/VERIFIED_CANNON.cfg"
curl -s -L -k "$LIST_URL" -o /tmp/links.txt

while read -r sub_url; do
    if [[ $sub_url == http* ]]; then
        curl -s -L -k --connect-timeout 5 "$sub_url" -o /tmp/sub_s.txt
        while read -r line; do
            if [[ $line == C:* ]]; then
                S=$(echo $line | awk '{print $2}')
                P=$(echo $line | awk '{print $3}')
                U=$(echo $line | awk '{print $4}')
                W=$(echo $line | awk '{print $5}')
                if [ ! -z "$S" ]; then
                    echo -e "[reader]\nlabel=Wolf_$S\nprotocol=cccam\ndevice=$S,$P\nuser=$U\npassword=$W\ngroup=1\nccckeepalive=1\ndisablecrccws=1\n" >> $OUTPUT2
                fi
            fi
        done < /tmp/sub_s.txt
    fi
done < /tmp/links.txt

rm /tmp/links.txt /tmp/sub_s.txt > /dev/null 2>&1
