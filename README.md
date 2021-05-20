# How to setup
Inside the config you will find `create-configmap.sh` execute it.

There is also ingress involved which means that you will have to add several address to your `/etc/hosts`. You can do it with:

```
echo "$(minikube ip) sa.database" | sudo tee -a /etc/hosts

echo "$(minikube ip) sa.flask" | sudo tee -a /etc/hosts
```

Then you are mostly ready to go. Database migration data could be found in `dump.sql`