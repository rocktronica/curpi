Curpi is an internet radio and amp, powered by a Raspberry Pi and housed in a cigar box, with an accompanying web GUI.

![Curpi](https://scontent-sjc2-1.cdninstagram.com/t51.2885-15/e35/12798126_1703767549870474_1581839300_n.jpg?ig_cache_key=MTIwMDk0MzYyOTExMjM0Mjk4MA%3D%3D.2)

## Running on boot

    sudo chown root.gpio /dev/mem
    sudo chmod g+rw /dev/mem

Then add `run.sh` to `/etc/rc.local`, substituting for your user name

    sudo -H -u USERNAME bash -c 'sh /home/USERNAME/curpi/run.sh &'

## License

MIT licensed or as components allow.
