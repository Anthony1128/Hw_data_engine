# Word Count with Hadoop

## Short description

Two reduce tasks were set. Custom partitioner was used with default algorithm (HashPartitioner).

Jar file is stored by path 'MapReduceHadoop/out/artifacts/MapReduceHadoop_jar/MapReduceHadoop.jar'

Java file is stored by path 'MapReduceHadoop/src/com/mypack/WordCount.java'

Project steps:

1. Having a jar file and input folder with test.txt file in HDFS (Initial state)
![Initial_state](./prntscrn0.png)

2. Starting a job by command: `hadoop jar MapReduceHadoop.jar com.mypack.WordCount /user/maria_dev/input /user/maria_dev/output`
![Start](./prntscrn1.png)

3. Finally, an output folder with two result files
![Result](./prntscrn2.png)
Content of first file
![Result](./prntscrn3.png)
Content of second file
![Result](./prntscrn4.png)