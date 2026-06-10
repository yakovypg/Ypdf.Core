# Usage
This document serves as a comprehensive guide for using **Ypdf.Core**.

## Build From Source
To [build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build) the library, run the following command from the project root.
```bash
dotnet build
```

## Run Tests
To [test](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test) the library, run the following command from the project root.
```bash
dotnet test
```

## Connect Project
At fitst, you need to clone **Ypdf.Core** repository and [add reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-add-reference) to the library:
```bash
dotnet add path_to_your_project.csproj reference path_to_lib/Core/Ypdf.Core
```

Next, you need to add the usings you need:
```cs
using Ypdf.Core.Tools;
```

Finally, you can work with the library.

### Step-By-Step Connection
Let's consider this step-by-step instructions for creating a sample project and connecting this library to it.
- Step 1: Go to the directory with your projects.
```bash
cd ~/Repos
```
- Step 2: Create folder for your project and move to it.
```bash
mkdir MyProject && cd MyProject
```
- Step 3: Create solution.
```bash
dotnet new sln
```
- Step 4: Create your project.
```bash
dotnet new console -o MyProject
```
- Step 5: Add your project to the solution.
```bash
dotnet sln add ./MyProject
```
- Step 6: Add folder for external projects and go to it.
```bash
mkdir Vendor && cd Vendor
```
- Step 7: Clone **Ypdf.Core** repository.
```bash
git clone https://github.com/yakovypg/Ypdf.Core.git
```
- Step 8: Move back to the root folder.
```bash
cd ..
```
- Step 9: Add **Ypdf.Core** to the solution.
```bash
dotnet sln add Vendor/Ypdf.Core/Core/Ypdf.Core
```
- Step 10: Move to your project folder.
```bash
cd MyProject
```
- Step 11: Add reference to the **Ypdf.Core**.
```bash
dotnet add reference ../Vendor/Ypdf.Core/Core/Ypdf.Core
```
- Step 12: Open Program.cs file and try using the **Ypdf.Core**.
```cs
using System;
using System.IO;
using Ypdf.Core.Tools;

const string inputPath = "/home/user/Downloads/input.pdf";
const string outputPath = "/home/user/Downloads/output.pdf";

var copyTool = new CopyTool();
copyTool.Execute(inputPath, outputPath);

bool ok = File.Exists(outputPath);
Console.WriteLine($"Success: {ok}");
```
- Step 13: Build the project.
```bash
dotnet build -c Release
```
- Step 14: Run the created application.
```bash
dotnet run
```
