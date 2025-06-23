# Symplique-Solutions.
azure-cost-opt-billing-records

# Azure Billing Record Cost Optimization

This repository contains a solution for reducing Azure Cosmos DB costs by archiving billing records older than 3 months to Blob Storage.

## Features
- Durable Function for background archival
- Fallback logic for reads from archive
- Zero API change
- Seamless migration with no downtime

## Components
- `archive_billing_records.py` – Moves old data to blob
- `read_handler.py` – Fallback read logic
- `write_handler.py` – Insert new records
- `blob_container_setup.ps1` – Blob setup script

 Architecture Diagram
 
                      ┌─────────────────────────────┐
                      │         Clients / API        │
                      └────────────┬────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │     Azure Function App       │
                    │ (Read/Write Billing Records) │
                    └───────┬──────────┬───────────┘
                            │          │
         ┌──────────────────▼──┐   ┌───▼─────────────────┐
         │  Cosmos DB (Hot DB) │   │ Azure Blob Storage  │
         │ Recent < 90 days    │   │ Archive > 90 days   │
         └──────────▲──────────┘   └──────────┬──────────┘
                    │                         │
       ┌────────────┴─────────────┐      ┌─────▼────────────────────┐
       │ Azure Durable Function   │◄─────┤ Timer-based Archiver Job │
       └──────────────────────────┘      └──────────────────────────┘


       
