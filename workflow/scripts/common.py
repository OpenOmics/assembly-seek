# Common helper functions shared across the entire workflow
import sys, os


def identify_samples_as_bam_fastq(samplelist, condition):
    """
    From sample names determines which of the input files have bam or fastq extensions.
    Pipeline uses this function's output to do quality check on fastqs
    and to convert bams to fastqs.
    @params samplelist list[<str>]:
        List of sample names wthout extensions
    @params condition dict[<str>]:
        A dictionary with sample name as key and its extension as value. 
    @return bam_samples list[<str>]:
        List of --input samples that have bam extension
    @return fastq_samples list[<str>]:
        List of --input samples that have fastq extension
    """
    bam_samples = []
    fastq_samples = []
    for sample in samplelist:
        if condition[sample] == "bam":
            bam_samples.append(sample)
        elif condition[sample] == "gz":
            fastq_samples.append(sample)
        else:
            sys.exit("Pipeline is not currently set up to process --input with {0} extensions, use either bam or fastq files!".format(condition[sample]))

    return bam_samples, fastq_samples


def provided(samplelist, condition):
    """
    Determines if optional rules should run. If an empty list is provided to rule all,
    snakemake will not try to generate that set of target files. If a given condition
    is not met (i.e. False) then it will not try to run that rule.
    """

    if not condition:
        # If condition is False, 
        # returns an empty list 
        # to prevent rule from 
        # running
        samplelist = []

    return samplelist


def ignore(samplelist, condition):
    """
    Determines if optional rules should run. If an empty list is provided to rule all,
    snakemake will not try to generate that set of target files. If a given condition
    is met (i.e. True) then it will not try to run that rule. This function is the 
    inverse to provided(). 
    """

    if condition:
        # If condition is True, 
        # returns an empty list 
        # to prevent rule from 
        # running
        samplelist = []

    return samplelist


def references(config, reflist):
    """
    Checks if a set of required reference files were provided. Some rules depend
    on a set of required reference files that may only exist for specific reference
    genomes. An example of this would be blasklists arriba. The blacklist are manually
    curated and only exist for a few reference genomes (mm10, hg38, hg19).
    If one of the required reference files does not exist, then it will return
    an empty list.
    """

    _all = True
    for ref in reflist:
        try: tmp = config['references'][ref]
        # Check if ref exists in config
        except KeyError:
            _all = False
            break
        # Check if ref is empty key string
        if not tmp: _all = False

    return _all


def allocated(resource, rule, lookup, default="__default__"):
    """Pulls resource information for a given rule. If a rule does not have any information 
    for a given resource type, then it will pull from the default. Information is pulled from
    definitions in the cluster.json (which is used a job submission). This ensures that any 
    resources used at runtime mirror the resources that were allocated.
    :param resource <str>: resource type to look in cluster.json (i.e. threads, mem, time, gres)
    :param rule <str>: rule to lookup its information
    :param lookup <dict>: Lookup containing allocation information (i.e. cluster.json)
    :param default <str>: default information to use if rule information cannot be found
    :return allocation <str>: 
        allocation information for a given resource type for a given rule
    """

    try: 
        # Try to get allocation information
        # for a given rule
        allocation = lookup[rule][resource]
    except KeyError:
        # Use default allocation information
        allocation = lookup[default][resource]
    
    return allocation


def str_bool(s):
    """Converts a string to boolean. It is dangerous to try to
    typecast a string into a boolean value using the built-in 
    `bool()` function. This function avoids any issues that can
    arise when using `bool()`. 
    Example:
      boolean('True') returns True
      boolean('False') returns False
      boolean('asdas') raises TypeError
    """
    val = s.lower()
    if val in ['true', '1', 'y', 'yes']:
        return True
    elif val in ['false', '0', 'n', 'no', '']:
        return False
    else:
        # Provided value could not be
        # type casted into a boolean
        raise TypeError('Fatal: cannot type cast {} into a boolean'.format(val))


def joint_option(prefix, valueslist):
    """Joins a list while adding a common prefix.
    Example:
      joint_option('-i', [1,2,3])
      '-i 1 -i 2 -i 3'
    """
    s = ""
    for v in valueslist:
        s += "{} {} ".format(prefix, v)
    s = s.rstrip()
    return s