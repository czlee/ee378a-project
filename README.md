# Fundamental limits in language modeling

*Chuan-Zheng Lee*<br/>
*EE 378A, Stanford University*

## Requisites
You need to have all of the following installed:
* **Julia**, with packages GZip, ArgParse and DataStructures
* **Python 2.7 and 3** (most scripts use Python 2, but one uses Python 3, sorry)
* **Matlab**

Then, obtain these estimators. Please pay attention to the instructions about symbolic links: scripts assume those links exist, and imports will fail if they are not set up correctly.

* The **Jiantao–Venkat–Han–Weissman (JVHW) estimator**, in Python, available by [cloning this repository](https://github.com/EEthinker/JVHW_Entropy_Estimators/).
    * Symbolic links pointing at `est_entro.py` and `poly_coeff_entro.mat` in the JVHW repository, should be made in the **python** directory, with the same names.
* The **profile maximum likelihood (PML) estimator**, in Python **and** Matlab, available by [cloning this repository](https://github.com/dmitrip/PML/).
    * A symbolic link pointing at `pml.py` in the PML repository, should be made in the **python** directory, with the same name.
    * For the Matlab version, the relevant scripts should be placed somewhere on the Matlab search path.
* The **Valiant and Valiant (VV) estimator**, in Matlab, available at http://theory.stanford.edu/~valiant/code.html.
    * Download the (standard, not-for-large-scale) code under "Estimating the Unseen". Its unzipped contents should be placed somewhere on the Matlab search path.

Of course, you can also copy the files rather than making symbolic links. The important thing is that it looks like the scripts `est_entro.py` and `pml.py`, and the data file `poly_coeff_entro.mat`, look like they are in the **python** directory.

## Obtaining the datasets

To run any of the scripts, you'll need to have the relevant datasets handy.

* **Penn Treebank.** If you're running this on Stanford's AFS, the scripts know where to find this data. If you're not, then you'll need to specify the directory for all scripts below that examine the PTB.
* **Web 1T 5-gram.** 
    * For unigrams through trigrams, if you're running this on Stanford's AFS, the scripts know where to find this data. If you're not, then you'll need to specify the directory for some of the scripts below. 
    * For quadrigrams and quintigrams, you'll need to specify the directory, where relevant. (The default option assumes they're in `/home/czlee/<n>gms/`; they presumably won't be on your computer.)
* **One Billion Words.** Follow the instructions to download and preprocess this data at https://github.com/ciprian-chelba/1-billion-word-language-modeling-benchmark. The scripts can operate on either the raw or processed (shuffled and tokenized) data, but I'd (strongly) recommend running on the processed data, because the processing also removes duplicates.

## Running the scripts

In every snippet, `<n>` should be replaced by the length of the _n_-gram in question, and `<n-prefix>grams` should be replaced with unigrams, bigrams, trigrams, _etc._ For each _n_, you need to run the script separately.

### Penn Treebank, naïve approach
```  bash
cd julia
julia ptb_frequencies.jl <n>     # this generates files that the naïve estimator then uses
julia naive.jl ptb <n>           # this does not write to any file itself
                                 # pipe the last line using `>` if you want to save results
```

### Penn Treebank, JVHW estimator
Make sure the JVHW symlinks are set up (see above).
``` bash
cd python
mkdirs ptb/jvhw
python penntreebank.py <n> -J ptb/jvhw/<n-prefix>grams.txt
```
You can use any output file name you want, but the `results_to_csv.py` script (#ptb-pml-and-ptb-vv)[below] assumes that the files will be called `unigrams.txt`, …, `septigrams.txt`. You can use any output directory you want, `results_to_csv.py` takes the directory name as its second argument. Saving the results to a known file is only important if you want to generate the evolution plots in the additional figure.

### Penn Treebank, PML estimator
``` bash
cd python
mkdir -p ptb/indices
python penntreebank.py <n> -Q ptb/indices/<n>grams.csv
```
Then start Matlab in the `matlab` directory and run `ptb_pml.m`. After the script has completed, final estimates will be in `estimates` and the progression of the estimate with increasing sample length will be in the cell array `progression`.

The file name `ptb/indices/<n>grams.csv` must be exactly as is: The Matlab script `ptb_vv.m` assumes the file will be in that location.

### Penn Treebank, VV estimator
``` bash
cd python
mkdir -p ptb/indices
python penntreebank.py <n> -Q ptb/indices/<n>grams.csv
```
Then start Matlab in the `matlab` directory and run `ptb_vv.m`. After the script has completed, final estimates will be in `estimates` and the progression of the estimate with increasing sample length will be in the cell array `progression`.

The file name `ptb/indices/<n>grams.csv` must be exactly as is: The Matlab script `ptb_vv.m` assumes the file will be in that location.

### Web 1T 5-gram, naïve approach
``` bash
cd julia
julia naive.jl 1t5 <n>           # this does not write to any file itself
                                 # pipe using `>` if you want to save results
```

### Web 1T 5-gram, JVHW estimator
``` bash
cd python
python web1t5gram_fingerprint.py <n> <n-prefix>grams-fingerprint.tsv
python web1t5gram_entropy.py <n-prefix>grams-fingerprint.tsv
```

You can use any file name you want, so long as the file name you pass to the first script is the same as the name you pass to the second script.

### One Billion Words, JVHW and PML estimators
The `-t` option gets it to examine the pretokenized data, not the raw data. The raw data is way too slow and contains lots of duplicates.
``` bash
cd python
mkdirs 1bw/entropy
python onebillionwords.py 5 -tJP 1bw/entropy/<n-prefix>grams-pretokenized.txt
```

You can use any output file name you want, but the `results_to_csv.py` script (#ptb-pml-and-ptb-vv)[below] assumes that the files will be called `unigrams-pretokenized.txt`, …, `sexigrams-pretokenized.txt`. You can use any output directory you want, `results_to_csv.py` takes the directory name as its second argument. Saving the results to a known file is only important if you want to generate the evolution plots in the additional figure.

## Generating evolution plots
*Note: The entropy rate and entropy rate estimate plots in the report aren't done on Matlab, they're just plotted directly in LaTeX using data manually transferred from the results of running the above. These instructions are for the plots in the* Additional Figures *of the report.*

### 1BW JVHW, 1BW PML and PTB JVHW

First, generate the CSV files that Matlab will use to generate these plots (this is the script that uses Python 3):
``` bash
cd python
python3 result_to_csv.py ptb ptb/jvhw jvhw
python3 result_to_csv.py 1bw 1bw/entropy jvhw
python3 result_to_csv.py 1bw 1bw/entropy pml
```

Then, change the first two lines of `entropy_plots.m` to the options you want, and run the script in Matlab.

### PTB PML and PTB VV

The files `ptb_pml.m` and `ptb_vv.m` must have been run before generating plots. (They save the results to `pml.mat` and `vv.mat` respectively.)

Change the first line to `ptb_plots.m` to the option you want, and run the script in Matlab.
