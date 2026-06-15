using System.Collections.Generic;
using Ypdf.Core.Config;
using Ypdf.Core.Extensions;
using Ypdf.Core.Runtime.Logging;
using Ypdf.Core.Runtime.Python;

namespace Ypdf.Core.Tools;

public class PdfToImageTool : PythonTool, IMultipleOutputTool
{
    public PdfToImageTool(
        int extractedImagesLimit = 0,
        string? pythonAlias = null,
        string? virtualEnvironmentPath = null,
        IOutputWriter? outputWriter = null)
        : base(pythonAlias, virtualEnvironmentPath, outputWriter)
    {
        ExtractedImagesLimit = extractedImagesLimit;
    }

    protected int ExtractedImagesLimit { get; init; }

    protected override IEnumerable<PythonPackage> VirtualEnvironmentPackages =>
    [
        new("PyMuPDF", "1.27.2.2")
    ];

    public override void Execute(string inputPath, string outputPath)
    {
        ExtendedArgumentException.ThrowIfNullOrWhiteSpace(inputPath, nameof(inputPath));
        ExtendedArgumentException.ThrowIfNullOrWhiteSpace(outputPath, nameof(outputPath));
        DefaultExceptions.ThrowIfFileNotExists(inputPath, nameof(inputPath));
        DefaultExceptions.ThrowIfDirectoryNotExists(outputPath, nameof(outputPath));

        inputPath = inputPath.Quoted();
        outputPath = outputPath.Quoted();

        string imageExtractorPath = PythonScriptPaths.ImageExtractor.Quoted();
        string args = $"{imageExtractorPath} -i {inputPath} -o {outputPath} -l {ExtractedImagesLimit}";

        PythonExecutor executor = CreateDefaultPythonExecutor();
        executor.Execute(args);
    }
}
