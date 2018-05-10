import sys
import os
import json

from azure.storage.blob.blockblobservice import BlockBlobService

from utils import get_container_names, get_blob_names_for_container

def parse_config(file_name):
    with open(file_name, "r") as f:
        data = json.loads(f.read())

    return data

if __name__ == "__main__":
    config = parse_config(os.path.join(".", "config.json"))

    os.chdir(config["download_path"])
    if not os.path.isdir(config["save_dir"]):
        os.mkdir(config["save_dir"])
    os.chdir(config["save_dir"])

    fileserver_download_path = os.path.abspath(".")

    if len(config["acc"]) == 0:
        print("[!] No accounts found in config.json")
        sys.exit(1)

    print("[+] %d accounts found." % len(config["acc"]))

    for account in config["acc"]:
        print("[+] Using account: %s" % account["account_name"])

        os.chdir(fileserver_download_path)
        if not os.path.isdir(account["account_name"]):
            os.mkdir(account["account_name"])
        os.chdir(account["account_name"])

        container_download_path = os.path.abspath(".")

        blob_service = BlockBlobService(**account)
        containers = get_container_names(blob_service)

        for bc in containers:
            print("  => Switched to container: %s" % bc)

            os.chdir(container_download_path)
            if not os.path.isdir(bc):
                os.mkdir(bc)
            os.chdir(bc)

            dp = os.path.abspath(".")

            blobs = get_blob_names_for_container(blob_service, bc)

            for bb in blobs:
                if os.path.exists(os.path.join(dp, bb)):
                    print("    <> File %s already exists, passing." % bb)
                    continue
                print("    => Downloading blob %s to path %s" % (bb, dp))
                blob_service.get_blob_to_path(bc, bb, os.path.join(dp, bb))

            print("")

        print("")
