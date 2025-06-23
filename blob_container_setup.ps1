# One-time setup of the blob container

$resourceGroup = "<your-resource-group>"
$storageAccount = "<your-storage-account>"
$containerName = "billing-archive"

az storage container create `
  --name $containerName `
  --account-name $storageAccount `
  --resource-group $resourceGroup `
  --public-access off
