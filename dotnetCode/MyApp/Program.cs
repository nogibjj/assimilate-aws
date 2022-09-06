// print the number of buckets in my s3 account on AWS
using System;
using Amazon.S3;
using Amazon.S3.Model;
namespace MyApp
{
    class Program
    {
        static void Main(string[] args)
        {
            var client = new AmazonS3Client();
            var response = client.ListBucketsAsync().Result;
            Console.WriteLine("Number of buckets: {0}", response.Buckets.Count);
        }
    }
}