for f in $(lxc ls -c n -f csv) ; do bash delete_snapshot.sh $f ; done
