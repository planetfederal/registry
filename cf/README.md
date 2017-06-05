# Cloud Foundry Registry App

In order to deploy registry to Cloud Foundry you will need to first create
the required services.

Note: Examples are for L2 PaaS version of PCF adjust the manifest.yml file as
needed for commercial PCF.

+ database (registry-db or what matches in your manifest.yml)

  ```bash
     if ! cf s | grep 'registry-db'; then
       cf cs pg_95_XL_DEV_SHARED_001 large-dev-100 registry-db -c cf/postgis.json;
     fi
  ```
  Note: the above uses a crunchydb service from the marketplace

+ index (api-search or what matches in your manifest.yml)

  ```bash
     if ! cf s | grep 'api-search'; then
       cf cups api-search -p "search_url";
     else cf uups api-search -p "search_url";
     fi
  ```
  Note: the above uses a user provided service and will prompt for the value
  for search_url.

Once the services have been created you will need to download the required
vendor files.

```bash
   pushd $REPO_ROOT/cf/vendor
   wget https://s3.amazonaws.com/api-paas-public/cfgeo-vendorlibs.0.0.1.cflinuxfs2.x86_64.tar.gz
   popd
```

Once the services have been created and vendor files downloaded you can then
push the app to cloudfoundry.

```bash
   cf push -f cf/manifest.yml
```
