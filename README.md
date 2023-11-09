# Introduction

In Spain, when it comes to medicinal products and their packaging, especially the data encoded in [Data Matrix GS1](https://www.gs1es.org/capturar-codigo-de-barras-gs1/gs1-datamatrix/) 2D barcodes, the following terms are commonly used:

* **PC** (Código Nacional): This is the "National Code" and represents a unique identifier for a specific drug product in Spain. It allows for quick identification and verification of a drug's legitimacy.

* **CAD** (Fecha de Caducidad): This translates to "Expiry Date" or "Expiration Date". It indicates until when the drug can be considered effective and safe to use.

* **SN** (Número de Serie): This stands for "Serial Number". As part of the EU's falsified medicines directive (FMD), medicines are serialized to prevent counterfeit medicines from entering the legitimate supply chain. Each pack will have a unique serial number to ensure traceability.

* **LOTE** (Número de Lote): This translates to "Batch Number" or "Lot Number". It is used to identify a specific batch of drugs for manufacturing and quality control purposes. If there's an issue with a specific batch, it can be traced and recalled if necessary.

These codes and identifiers help ensure patient safety and the authenticity and traceability of drugs in the supply chain.

See more info at:

[https://www.aemps.gob.es/industria/dispositivos_seguridad/FAQs/home.htm](https://www.aemps.gob.es/industria/dispositivos_seguridad/FAQs/home.htm)

# The Problem

As odd as it may sound, the 4 codes are embedded within a barcode and whoever encoded them didn't use the appropriate anchor terms, nor did they maintain a specific order. In essence, these four terms can be randomly positioned within a string, distinguished by certain characters:

* `01` denotes the PC (PC) that comes after.
* `21` represents the Serial Number that follows.
* `10` points to the Lot/Batch Number that comes next.
* `17` signifies the Expiry Date following it.

In theory, this might sound straightforward, but in practice, various separators can be encountered. Moreover, these codes might themselves include the separators. This complexity makes parsing quite a challenge. This is precisely why I devised this Perl Module.

I crafted this script in my leisure to aid my sister, who is a pharmacist, and had been manually inputting LOTE into Excel.

Included in the script is a folder named `macro`, where, as the name suggests, you can store a macro to run it in Excel.

# Notes

The script is expecting **raw** barcodes such as those coming from a mobile phone App (i.e., without any post-processing such as parenthesis, etc.).

The performance is relatively good ... it captures (approximate values):

* `PC`   - 90%
* `SN`   - 90%
* `LOTE` - 100%
* `CAD`  - 100%

When it fails is because there is an overlapping pattern inside a code, making almost impossible to be captured. Find below an example:

QR:`010847000700681721PE42EEADPA9HW41728033110V067127006817` 

PC: `8470007006817`

PC proposed: `84700070068`

It fails because the 17 is pruned at the tail because it was expacting to be the anchor for `CAD`.

If you are able to come up with a better solution please let me know.

I hope this code helps you.

NB: The module is basically four regex. I am not planning in submitting it to CPAN. Or to translate to Python. Or Javascript.

Cheers!

Manu

# Download and Installation

## Step 1: Install `Cpanminus`

    curl -L https://cpanmin.us | perl - App::cpanminus

## Step 2: Download and install from Github

    git clone https://github.com/mrueda/datamatrix2codes.git
    cd datamatrix2codes
    cpanm --local-lib=~/perl5 local::lib && eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
    cpanm --notest --installdeps .
    ./datamatrix2codes.pl data/codes.csv 

By default, the output will be saved as `output.csv`. You can specify another name for the files as:

    ./datamatrix2codes.pl data/codes.csv other_output.csv

## System requirements

    * Ideally a Debian-based distribution (Ubuntu or Mint), but any other (e.g., CentOs, OpenSuse) should do as well.
    * Perl 5 (>= 5.16 core; installed by default in most Linux distributions). Check the version with "perl -v".
    * >= 1GB of RAM
    * 1 core

# AUTHOR 

Written by Manuel Rueda, PhD.

# COPYRIGHT AND LICENSE

This PERL file is copyrighted. See the LICENSE file included in this distribution.
