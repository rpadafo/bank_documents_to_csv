# Bank documents exports to CSV
Convert all documents in Excel or TXT format from Spanish banks into CSV files so they can be imported into Actual Budget

---

> [!IMPORTANT]
> It is necesary to have Actual Budget installed. You also need Docker and a folder to storage the EXCELS and CSV documents

## Features

At this moment you can only use this banks:
 * Bankinter (Excel)
 * Caixa bank now (Excel)
 * Santander (Excel)
 * Sabadell (TXT)

## Usage

You can install this app with docker. You can use our `docker-compose_EXAMPLE` file to start.

```yaml
services:
  bank_documents_to_csv:
    image: ghcr.io/rpadafo/bank_documents_to_csv:latest
    container_name: bankdocumentstocsv
    restart: unless-stopped
    environment:
      - RETENTION_HOUR=12
    deploy:
        resources:
            limits:
                cpus: '1'
                memory: 100M
    volumes:
      # Two folders required, excel and CSV >>
      - ./excel:/excel
      - ./csv:/csv
```

Then you only need to copy the documents from the banks to the EXCEL folder and the app transform it into CSV, so you can import this files to Actual Budget.

## Actual Budget
You need to setup each bank in Actual Budget, and import each CSV to each bank.

> [!TIP]
> For Sabadell, it is not a CSV, so you need to choose the | symbol for field separator. For Sabadell, only change the extension of the file, but the content is the same.