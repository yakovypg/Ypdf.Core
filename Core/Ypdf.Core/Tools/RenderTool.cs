using System.Collections.Generic;
using System.Linq;
using Ypdf.Core.Config;
using Ypdf.Core.Enumeration;
using Ypdf.Core.Extensions;
using Ypdf.Core.Imaging;
using Ypdf.Core.Runtime.Logging;
using Ypdf.Core.Runtime.Python;

namespace Ypdf.Core.Tools;

public class RenderTool : PythonTool, IMultipleOutputTool
{
    public RenderTool(
        IEnumerable<PageRange>? pages,
        string? pythonAlias = null,
        string? virtualEnvironmentPath = null,
        IOutputWriter? outputWriter = null)
        : this(
            pages,
            new ImageRendering(),
            pythonAlias,
            virtualEnvironmentPath,
            outputWriter)
    { }

    public RenderTool(
        IEnumerable<PageRange>? pages,
        ImageRendering imageRendering,
        string? pythonAlias = null,
        string? virtualEnvironmentPath = null,
        IOutputWriter? outputWriter = null)
        : this(
            PageRange.GetAllItems(pages ?? []),
            imageRendering,
            pythonAlias,
            virtualEnvironmentPath,
            outputWriter)
    { }

    public RenderTool(
        IEnumerable<int>? pages,
        string? pythonAlias = null,
        string? virtualEnvironmentPath = null,
        IOutputWriter? outputWriter = null)
        : this(
            pages,
            new ImageRendering(),
            pythonAlias,
            virtualEnvironmentPath,
            outputWriter)
    { }

    public RenderTool(
        IEnumerable<int>? pages,
        ImageRendering imageRendering,
        string? pythonAlias = null,
        string? virtualEnvironmentPath = null,
        IOutputWriter? outputWriter = null)
        : base(pythonAlias, virtualEnvironmentPath, outputWriter)
    {
        Pages = pages;
        ImageRendering = imageRendering;
    }

    protected IEnumerable<int>? Pages { get; }
    protected ImageRendering ImageRendering { get; }

    protected override IEnumerable<PythonPackage> VirtualEnvironmentPackages =>
    [
        new("pdf2image", "1.17.0")
    ];

    public override void Execute(string inputPath, string outputPath)
    {
        ExtendedArgumentException.ThrowIfNullOrWhiteSpace(inputPath, nameof(inputPath));
        ExtendedArgumentException.ThrowIfNullOrWhiteSpace(outputPath, nameof(outputPath));
        DefaultExceptions.ThrowIfFileNotExists(inputPath, nameof(inputPath));
        DefaultExceptions.ThrowIfDirectoryNotExists(outputPath, nameof(outputPath));

        inputPath = inputPath.Quoted();
        outputPath = outputPath.Quoted();

        string pdfRendererPath = PythonScriptPaths.PdfRenderer.Quoted();
        string args = $"{pdfRendererPath} -i {inputPath} -o {outputPath} -d {ImageRendering.Dpi}";

        if (!string.IsNullOrWhiteSpace(ImageRendering.Extension))
            args += $" -e {ImageRendering.Extension}";

        if (Pages is not null && Pages.Any())
        {
            string pagesPresenter = string.Join(" ", Pages);
            args += $" -p {pagesPresenter}";
        }

        PythonExecutor executor = CreateDefaultPythonExecutor();
        executor.Execute(args);
    }
}
