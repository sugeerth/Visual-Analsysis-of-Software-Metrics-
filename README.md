# Visual Analysis of Software Code Evolution#

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

It is well-established in the literature that software complexity metrics which includes code complexity, process, and social metrics have a high correlation with bugs in software. Though this is known and accepted, these metrics can sometimes be difficult to conceptualize for those who are not experts in the field. In addition, predictive models are built on average case behavior, while the ecosystem of a particular project may have fine-grained details that stray from the norm. Also, when considering a system over time, understanding complex dynamics between changing parts makes understanding much more difficult. This project will provide a tool that aids in visualizing metrics and system evolution at varying granularities that allow a security analyst to be able to spot potential problems in a system. In addition, we aim to provide further evidence of useful metrics in predicting bugs - specifically security vulnerabilities. To show this, we will use data gathered from the Apache Software Foundation projects and use an established strategy of linking bugs to bug-introducing and bug-fixing commits. We will then overlay mined CVE(Common Vulnerability Exposure) data with these bugs to examine our precision and recall. All of the information gained from this process will be fed back into the visualization tool, providing a useful look at the projects under study. Ideally, our goal for the tool is to have it operate on any software system that uses Git for version control.
https://www.youtube.com/watch?v=eUnrEkfbQjw

### How do I get set up? ###

Basically the steps to set up are: 

1) We have sampel data in the data folder, if you would want to recreate your own data then sanitize/rearrange your data by running the script dataModel.py and change your data file name in the file accordingly 

2) Change the path of the data in the ApplicationHandler.py script 

3) Witness the magic performed by the tool. 

4) See your code in visual elements. 
