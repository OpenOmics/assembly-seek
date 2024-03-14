# <code>assembly-seek <b>run</b></code>

## 1. About 
The `assembly-seek` executable is composed of several inter-related sub commands. Please see `assembly-seek -h` for all available options.

This part of the documentation describes options and concepts for <code>assembly-seek <b>run</b></code> sub command in more detail. With minimal configuration, the **`run`** sub command enables you to start running assembly-seek pipeline. 

Setting up the assembly-seek pipeline is fast and easy! In its most basic form, <code>assembly-seek <b>run</b></code> only has *two required inputs*.

## 2. Synopsis
```text
$ assembly-seek run [--help] \
    [--dry-run] [--job-name JOB_NAME] [--mode {slurm,local}] \
    [--sif-cache SIF_CACHE] [--singularity-cache SINGULARITY_CACHE] \
    [--silent] [--threads THREADS] [--tmp-dir TMP_DIR] \
    [--assemblers flye raven hifiasm] \
    [--genome-size GENOME_SIZE] \
    [--coverage COVERAGE] \
    [--lineage-name LINEAGE_NAME] \
    --input INPUT [INPUT ...] \
    --output OUTPUT
```

The synopsis for each command shows its arguments and their usage. Optional arguments are shown in square brackets.

A user **must** provide a list of HiFi CCS FastQ (globbing is supported) or BAM files to analyze via `--input` argument and an output directory to store results via `--output` argument.

Use you can always use the `-h` option for information on a specific command. 

### 2.1 Required arguments

Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.

  `--input INPUT [INPUT ...]`  
> **Input HiFi CCS FastQ or BAM file(s).**  
> *type: file(s)*  
> 
> One or more HiFi CCS FastQ or BAM files can be provided. From the command-line, each input file should seperated by a space. Globbing is supported! This makes selecting input files easy. Input FastQ files should always be gzipp-ed.
> 
> ***Example:*** `--input .tests/*.R?.fastq.gz`

---  
  `--output OUTPUT`
> **Path to an output directory.**   
> *type: path*
>   
> This location is where the pipeline will create all of its output files, also known as the pipeline's working directory. If the provided output directory does not exist, it will be created automatically.
> 
> ***Example:*** `--output /data/$USER/assembly-seek_out`

### 2.2 Analysis options

Each of the following arguments are optional, and do not need to be provided.  

  `--assemblers ASSEMBLER [ASSEMBLER ...]`
> **Genome assembler(s)**  
> *type: string*  
> *default: `flye raven hifiasm`*  
>
> A list of de-novo long read genome assemblers to use. Please choose from the following list of supported assemblers: ["flye", "raven", "hifiasm"].
>
> ***Example:*** `--assemblers flye raven`  

---  
  `--genome-size GENOME_SIZE`
> **Estimated genome size.**  
> *type: string*  
> *default: none*  
>
> This is the estimated size of the organism's genome in Mb or Gb. This option is used with flye assembler only. Please note: this option MUST be used with the `--coverage` option (see below).
>
> ***Example:*** `--genome-size 23.5m`  

---  
  `--coverage COVERAGE`  
> **Reduces coverage for initial assembly.**  
> *type: int*  
> *default: none*  
>
> Typically, assemblies of large genomes at high coverage require several hundreds of RAM. For high coverage datasets, you can reduce memory usage by using only a subset of longest reads for initial disjointig extension stage (which is usually the memory bottleneck). This option specifies the target coverage of the longest reads. It is worth noting that setting this option to 40 is usually enough to produce good disjointigs. Regardless of how this option is set, all reads will be used at the later pipeline stages (e.g. for repeat resolution). This option is used with the flye assembler only. Please note: this option MUST be used with the `--genome-size` option.
>
> ***Example:*** `--coverage 20`  

---  
  `--lineage-name LINEAGE_NAME`  
> **Busco lineage name.**  
> *type: string*  
> *default: none*  
>
> This option can be provided to specify the name of the BUSCO lineage to be used. If provided, please provide a valid busco lineage name from the following [link](https://busco-archive.ezlab.org/data/lineages/). If the provided database for your lineage name does not exist locally, it will be downloaded into your output directory. By default, the pipeline will run using busco's auto-lineage option to find the closest lineage in its eukaryota, bacteria, and archaea databases.
>
> ***Example:*** `--lineage-name diptera_odb10`  

### 2.3 Orchestration options

Each of the following arguments are optional, and do not need to be provided. 

  `--dry-run`            
> **Dry run the pipeline.**  
> *type: boolean flag*
> 
> Displays what steps in the pipeline remain or will be run. Does not execute anything!
>
> ***Example:*** `--dry-run`

---  
  `--silent`            
> **Silence standard output.**  
> *type: boolean flag*
> 
> Reduces the amount of information directed to standard output when submitting master job to the job scheduler. Only the job id of the master job is returned.
>
> ***Example:*** `--silent`

---  
  `--mode {slurm,local}`  
> **Execution Method.**  
> *type: string*  
> *default: slurm*
> 
> Execution Method. Defines the mode or method of execution. Vaild mode options include: slurm or local. 
> 
> ***slurm***    
> The slurm execution method will submit jobs to the [SLURM workload manager](https://slurm.schedmd.com/). It is recommended running assembly-seek in this mode as execution will be significantly faster in a distributed environment. This is the default mode of execution.
>
> ***local***  
> Local executions will run serially on compute instance. This is useful for testing, debugging, or when a users does not have access to a high performance computing environment. If this option is not provided, it will default to a local execution mode. 
> 
> ***Example:*** `--mode slurm`

---  
  `--job-name JOB_NAME`  
> **Set the name of the pipeline's master job.**  
> *type: string*
> *default: pl:assembly-seek*
> 
> When submitting the pipeline to a job scheduler, like SLURM, this option always you to set the name of the pipeline's master job. By default, the name of the pipeline's master job is set to "pl:assembly-seek".
> 
> ***Example:*** `--job-name pl_id-42`

---  
  `--singularity-cache SINGULARITY_CACHE`  
> **Overrides the $SINGULARITY_CACHEDIR environment variable.**  
> *type: path*  
> *default: `--output OUTPUT/.singularity`*
>
> Singularity will cache image layers pulled from remote registries. This ultimately speeds up the process of pull an image from DockerHub if an image layer already exists in the singularity cache directory. By default, the cache is set to the value provided to the `--output` argument. Please note that this cache cannot be shared across users. Singularity strictly enforces you own the cache directory and will return a non-zero exit code if you do not own the cache directory! See the `--sif-cache` option to create a shareable resource. 
> 
> ***Example:*** `--singularity-cache /data/$USER/.singularity`

---  
  `--sif-cache SIF_CACHE`
> **Path where a local cache of SIFs are stored.**  
> *type: path*  
>
> Uses a local cache of SIFs on the filesystem. This SIF cache can be shared across users if permissions are set correctly. If a SIF does not exist in the SIF cache, the image will be pulled from Dockerhub and a warning message will be displayed. The `assembly-seek cache` subcommand can be used to create a local SIF cache. Please see `assembly-seek cache` for more information. This command is extremely useful for avoiding DockerHub pull rate limits. It also remove any potential errors that could occur due to network issues or DockerHub being temporarily unavailable. We recommend running assembly-seek with this option when ever possible.
> 
> ***Example:*** `--singularity-cache /data/$USER/SIFs`

---  
  `--threads THREADS`   
> **Max number of threads for each process.**  
> *type: int*  
> *default: 2*
> 
> Max number of threads for each process. This option is more applicable when running the pipeline with `--mode local`.  It is recommended setting this vaule to the maximum number of CPUs available on the host machine.
> 
> ***Example:*** `--threads 12`


---  
  `--tmp-dir TMP_DIR`   
> **Max number of threads for each process.**  
> *type: path*  
> *default: `/lscratch/$SLURM_JOBID`*
> 
> Path on the file system for writing temporary output files. By default, the temporary directory is set to '/lscratch/$SLURM_JOBID' for backwards compatibility with the NIH's Biowulf cluster; however, if you are running the pipeline on another cluster, this option will need to be specified. Ideally, this path should point to a dedicated location on the filesystem for writing tmp files. On many systems, this location is set to somewhere in /scratch. If you need to inject a variable into this string that should NOT be expanded, please quote this options value in single quotes.
> 
> ***Example:*** `--tmp-dir /scratch/$USER/`

### 2.4 Miscellaneous options  
Each of the following arguments are optional, and do not need to be provided. 

  `-h, --help`            
> **Display Help.**  
> *type: boolean flag*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** `--help`

## 3. Example
```bash 
# Step 1.) Grab an interactive node,
# do not run on head node!
srun -N 1 -n 1 --time=1:00:00 --mem=8gb  --cpus-per-task=2 --pty bash
module purge
module load singularity snakemake

# Step 2A.) Dry-run the pipeline
./assembly-seek run --input .tests/*.R?.fastq.gz \
                  --output test_01 \
                  --mode slurm \
                  --dry-run

# Step 2B.) Run the assembly-seek pipeline
# The slurm mode will submit jobs to 
# the cluster. It is recommended running 
# the pipeline in this mode.
./assembly-seek run --input .tests/*.R?.fastq.gz \
                  --output test_01 \
                  --mode slurm
```