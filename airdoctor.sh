#!/bin/bash

AIRDOCTOR_IMAGE=${AIRDOCTOR_IMAGE:-"airbyte/airdoctor"}
AIRDOCTOR_TAG=${AIRDOCTOR_TAG:-"latest"}

AIRDOCTOR_MODE=${AIRDOCTOR_MODE:-"local"}

# Utilities
error() { echo "$@" 1>&2 ; exit 1; }



main() {
    return 0
}

main "$@"
