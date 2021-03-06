# Getting Started with ModelDB on spark.ml

## 1. Clone the repo

```git
git clone https://github.com/mitdbg/modeldb
```

## 2. Install dependencies
We assume that you have Java 1.8+ and Spark 2.0 installed.

**Versions**: ModelDB currently requires **Thrift 0.9.3** and **Spark 2.0**.

On Mac OSX:

```bash
brew install sqlite
brew install maven
brew install node
brew install sbt

# we require Thrift 0.9.3 at the moment (brew install will give you 0.10.1)
Download 0.9.3 from: http://archive.apache.org/dist/thrift/0.9.3/
Follow build instructions at: https://thrift.apache.org/docs/install/os_x
```

On Linux:

```bash
apt-get update
sudo apt-get install sqlite
sudo apt-get install maven
sudo apt-get install sbt
sudo apt-get install nodejs # may need to symlink node to nodejs. "cd /usr/bin; ln nodejs node"

# install thrift. path_to_thrift is the installation directory
cd path_to_thrift
wget http://mirror.cc.columbia.edu/pub/software/apache/thrift/0.9.3/thrift-0.9.3.tar.gz
tar -xvzf thrift-0.9.3.tar.gz
cd thrift-0.9.3
./configure
make
export PATH=path_to_thrift/:$PATH
```
For more help on installing dependencies see [here](https://github.com/mitdbg/modeldb/blob/master/docs/required_software.md).

## 3. Build

ModelDB is composed of three components: the ModelDB server, the ModelDB client libraries, and the ModelDB frontend.

In the following, **path_to_modeldb** refers to the directory into which you have cloned the modeldb repo.

```bash
# build and start the server
cd path_to_modeldb/server
cd codegen
./gen_sqlite.sh
cd ..
./start_server.sh &

# build spark.ml client library
cd path_to_modeldb/client/scala/libs/spark.ml
./build_client.sh

# start the frontend
cd path_to_modeldb/frontend
./start_frontend.sh &

```

## 4. Incorporate ModelDB into an ML workflow

#### a. Import the ModelDB client library classes

```scala
import edu.mit.csail.db.ml.modeldb.client._
import edu.mit.csail.db.ml.modeldb.client.ModelDbSyncer._

```

#### b. Create a ModelDB syncer
ModelDBSyncer is the object that logs models and operations to the ModelDB backend. You can initialize the syncer either from a config file (e.g. [modeldb/client/scala/libs/spark.ml/syncer.json](https://github.com/mitdbg/modeldb/blob/master/client/scala/libs/spark.ml/syncer.json)) or explicitly via arguments.

```scala
// initialize syncer from config file
ModelDbSyncer.setSyncer(new ModelDbSyncer(SyncerConfig(path_to_config)))
```
OR
```scala
// initialize syncer explicitly
ModelDbSyncer.setSyncer(
      // what project are you working on
      new ModelDbSyncer(projectConfig = NewOrExistingProject(
        "Demo", // project name
        "modeldbuser", // user name
        "Project to hold all models from the demo" // project description
      ),
      experimentConfig = new DefaultExperiment,
      experimentRunConfig = new NewExperimentRun
      )
    )

```

#### c. Log models and pre-processing operations
Next use the ModelDB **sync** variants of functions. So _fit_ calls would turn into **fitSync**, _save_ calls would turn into **saveSync** and so on.

```scala
val logReg = new LogisticRegression()
val logRegModel = logReg.fitSync(trainDf)
val predictions = logRegModel.transformSync(test)

logRegModel.saveSync("simple_lr")

```

#### d. Log metrics
Use the ModelDB metrics class (**SyncableMetrics**) or use the spark Evaluator classes with the **evaluateSync** method. 

```scala
val metrics = SyncableMetrics.ComputeMulticlassMetrics(lrModel, predictions, labelCol, predictionCol)

```
OR
```scala
val evaluator = new BinaryClassificationEvaluator()
val metric = evaluator.evaluateSync(predictions, logRegModel)
```
<!-- At the end of your workflow, be sure to sync all the data with ModelDB.
```scala
 ModelDbSyncer.sync()
```
-->

The full code for this example can be found [here](https://github.com/mitdbg/modeldb/blob/master/client/scala/libs/spark.ml/src/main/scala-2.11/edu/mit/csail/db/ml/modeldb/sample/SimpleSample.scala).

#### e. _Run your program!_

Be sure to link the client library built above to your code (e.g. by adding to your classpath).

## 5. Explore models
That's it! Explore the models you built in your workflow at [http://localhost:3000](http://localhost:3000).

<img src="images/frontend-1.png">

**More complex spark.ml workflows using ModelDB are located [here](https://github.com/mitdbg/modeldb/tree/master/client/scala/libs/spark.ml/src/main/scala-2.11/edu/mit/csail/db/ml/modeldb/sample) and [here](https://github.com/mitdbg/modeldb/tree/master/client/scala/libs/spark.ml/src/main/scala-2.11/edu/mit/csail/db/ml/modeldb/evaluation)**
