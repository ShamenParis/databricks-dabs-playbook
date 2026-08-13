import argparse
from pyspark.sql import SparkSession

# Parse dynamic job parameters passed from DABs
parser = argparse.ArgumentParser(description="Job Parameters Example")
parser.add_argument("--env", type=str, required=True, help="Environment name (e.g., dev, prod)")
parser.add_argument("--greeting", type=str, required=True, help="Custom greeting message")
args = parser.parse_args()

print(f"🚀 Initializing job in [{args.env.upper()}] environment...")
print(f"Message received: {args.greeting}")

# Initialize Spark session
spark = SparkSession.builder.appName(f"JobParams_{args.env}").getOrCreate()

# Create a sample DataFrame to prove the parameters were passed successfully
data = [("Environment", args.env), ("Greeting", args.greeting)]
df = spark.createDataFrame(data, ["Parameter", "Value"])

print("✅ Parameters successfully loaded into the DataFrame:")
df.show()