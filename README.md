# amphib

Generates some additional information for amphibians based on
[Amphibian Species of the World Database](http://research.amnh.org/vz/herpetology/amphibia/index.php/)
and [AmphibiaWeb](http://amphibiaweb.org/data/access.html). You can download
the full species list from AmphibiaWeb [here](http://amphibiaweb.org/amphib_names.txt).

The main difference between these two databases is that AmphibiaWeb do not provide information on the:
 * authors who described the species and also the year of description.
 * type locality: where the species was first observed in nature
 * distribution: general information on distribution of a given species.

This process will add the additional columns as necessary.

## How to use:

### Using virtualenv (recommended)
Best way to use this is to use [virtualenv](http://virtualenv.readthedocs.io/en/stable/installation/)

Clone the repo
```
git clone https://github.com/funkycoda/amphib.git
```

Navigate to the folder and enable it for ```virtualenv```
```
cd amphib
virtualenv .
source bin/activate
```

Install the necessary dependencies
```
pip install -r requirements.txt
```
