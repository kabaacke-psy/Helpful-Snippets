# Helpful Snippets

## Description

**What this is:**
- Tips, Tricks, and Suggestions

    This repository contains commented segments of code which can be copied, pasted, and modified in order to expedite the generation of code to run analytical pipelines on or off of a cluster environment. 
 
- Collaborative

    This is a collaborative project. The code is has been inspired by countless other GitHub repositories, Stack Overflow posts, Blogs, and helpful collaborators from academia and industry. All users are encouraged to submit their additions through pull requests. Be sure to add your name to the author list in your pull request! (for information on pull requests, please see here(insert link here).

**What this is NOT**
- A comprehensive guide.
- A replacement for Googling issues and generating your own creative solutions.
- The only way of doing these things.
- The 'best' way of doing things.
- Proprietary in any way.
- Exclusive to any user or group.

## Getting Started

### Dependencies
The contents of this repository cover a range of topics, and you may only require a small subset of these dependencies to complete your pipeline. All code has been tested using the following specifications:

- Python            3.8.5 and 3.9.2
    - pandas        1.2.2
    - numpy         1.20.1
    - paramiko      2.7.2
    - scp           0.14.1
    - DateTime      4.3
    - joblib        1.0.1
- R                 4.0.4
    - reticulate    1.22

## Help
Most files will contain a commented link or links to further information. If your questions are not answered using the link(s), try searching your issue. If you find an answer to your question, consider adding the information you found to the repository and submitting a pull request! You can answer the question for the next user!

## Contents
- In Progress

  *Files or placeholders for scripts which have not been completed or fully documented*
- Resources

  *Dependencies or references for snippets and runnables*
- Runnables

  *Files configured to be run via command line interface*
- Snippets

  *Notebooks or code files documenting how to accomplish various processes*
  - Metadata Tracking
    - *uid_metadata_tracking.ipynb*: 
    
      There are at least as many naming conventions for files as there are researchers. Contrary to most naming conventions using abbreviations stringed together, this snippet describes a way to track as many researcher degrees of freedom (analysis metadata) as you would like, without lengthening the file name. Instead of attaching this metadata information to each file by embedding the information in the file name, the prefix or suffix on the file name is a unique identifier \{UID\} that points to a separate metadata file. This metadata file (\{UID\}_metadata.json) can contain as many key, value pairs as you want for any given pipeline. This removes any enticement to limit the number of metadata attributes saved on each run, further enabling reproducibility through clarity in analytic choices.
  - Running in Parallel
    - *calling_in_parallel_shell.ipynb*: 
    
      This snippet provides an example of how to do so without the use of any non-generic packages or functions within a bash environment. This can enable you to make full use of the compute resources available without the additional overhead of installing other tools. The process can be divided into 3 main steps: 1) establishing the resource pool available to use, 2) defining a function to run in parallel if there are multiple components of a process that need to be run for each iteration, and 3) calling the function in parallel. This snippet will go through each process with an example which callas a python script using variables in nested for loops.


## Authors
- Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy


## Version History

*Unreleased*

## License

This project is licensed under the Unlicense - see the LICENSE.md file for details

## Acknowledgments
It takes a village, and there have been countless direct and indirect intellectual contributions to this work outside of the list of authors. A huge thanks to all of these people for the feedback, inspiration, and facilitation of the processes involved in the creation of this work!

- Corey Richier
- Megan Finnegan
- Wendy Heller
- Gregory Miller
- Ramsey Wilcox
- Paul Bogden
