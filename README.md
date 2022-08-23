A simple script update CloudFlare DDNS for Synology NAS. This script can be
integrated into Synology NAS UI. It largely refers to
[official CloudFlare's API example for Python](https://raw.githubusercontent.com/cloudflare/python-cloudflare/master/examples/example_update_dynamic_dns.py)

# Installation

1.  Install python3 from synology package using the NAS web interface.
2.  Enable the SSH connection and ssh into your NAS
3.  Install pip for python3, then get python-cloudflare

```
sudo python3 -m ensurepip
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install git+https://github.com/butlerx/SynologyCloudflareDDNS.git#egg=synology_cloudflare_ddns
```

5.  (optional) You can firstly test the script's functionality. Running this
    script without any arguments gives the usage, like
    `python3 -m synology_cloudflare_ddns <username> <api_key> <hostname> <ip_address>`
    `username` is your CloudFlare username, usually the email address you
    registered in CloudFlare. `api_key` is your personal CloudFlare API key. See
    [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-)
    in how to retrive the key.
6.  Integrate the script into Synology DDNS management interface by adding the
    following text into `/etc.defaults/ddns_provider.conf`

```
[Cloudflare]
        modulepath=/usr/local/bin/cloudflareDDNS.py
        queryurl=https://www.cloudflare.com/
```

7.  Go to DDNS management page in your NAS web UI (control->external
    access->DDNS). Click Add. And select Cloudflare from the drop-down menu.
    Fill the three necessary fields which are hostname, username, and
    password(CloudFlare API Key).

That's it. See if the DDNS' IP has been updated in your Cloudflare page.
