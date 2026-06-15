# Tools
Here you can see instructions for working with tools.

## Existing Tools
**Ypdf.Core** has the following tools:
- [GetInfoTool](/Core/Ypdf.Core/Tools/GetInfoTool.cs): Get PDF document information
- [SplitTool](/Core/Ypdf.Core/Tools/SplitTool.cs): Split PDF document
- [MergeTool](/Core/Ypdf.Core/Tools/MergeTool.cs): Merge PDF documents
- [CompressTool](/Core/Ypdf.Core/Tools/CompressTool.cs): Compress PDF document
- [CopyTool](/Core/Ypdf.Core/Tools/CopyTool.cs): Copy PDF document
- [RemovePageTool](/Core/Ypdf.Core/Tools/RemovePageTool.cs): Remove pages from PDF document
- [MovePageTool](/Core/Ypdf.Core/Tools/MovePageTool.cs): Move PDF document page
- [MovePageTool](/Core/Ypdf.Core/Tools/MovePageTool.cs): Reorder PDF document pages
- [RotateTool](/Core/Ypdf.Core/Tools/RotateTool.cs): Rotate PDF document pages
- [CropPageTool](/Core/Ypdf.Core/Tools/CropPageTool.cs): Crop PDF document pages
- [DividePageTool](/Core/Ypdf.Core/Tools/DividePageTool.cs): Divide PDF document pages
- [ResizePageTool](/Core/Ypdf.Core/Tools/ResizePageTool.cs): Resize PDF document pages
- [AddPageNumbersTool](/Core/Ypdf.Core/Tools/AddPageNumbersTool.cs): Add page numbers to PDF document
- [AddIndelibleWatermarkTool](/Core/Ypdf.Core/Tools/AddIndelibleWatermarkTool.cs), [AddWatermarkAnnotationTool](/Core/Ypdf.Core/Tools/AddWatermarkAnnotationTool.cs): Add watermark to PDF document
- [RemoveWatermarkAnnotationTool](/Core/Ypdf.Core/Tools/RemoveWatermarkAnnotationTool.cs): Remove watermark from PDF document
- [ImageToPdfTool](/Core/Ypdf.Core/Tools/ImageToPdfTool.cs): Convert images to PDF document
- [TextToPdfTool](/Core/Ypdf.Core/Tools/TextToPdfTool.cs): Convert text to PDF document
- [ExtractImagesTool](/Core/Ypdf.Core/Tools/ExtractImagesTool.cs): Extract images from PDF document
- [ExtractTextTool](/Core/Ypdf.Core/Tools/ExtractTextTool.cs), [ExtractTextSimpleTool](/Core/Ypdf.Core/Tools/ExtractTextSimpleTool.cs): Extract text from PDF document
- [SetPasswordTool](/Core/Ypdf.Core/Tools/SetPasswordTool.cs): Set password to PDF document
- [RemovePasswordTool](/Core/Ypdf.Core/Tools/RemovePasswordTool.cs): Remove password from PDF document
- [CompressImageTool](/Core/Ypdf.Core/Tools/CompressImageTool.cs): Compress images

## Add Custom Tool
You can add a custom tool by creating a class that implements one of the following interfaces:: `ITool`, `IMultipleInputTool`, `IMultipleOutputTool`, or `ICheckingTool`. Then implement the chosen interface. For an example, see [CopyTool](/Core/Ypdf.Core/Tools/CopyTool.cs), [MergeTool](/Core/Ypdf.Core/Tools/MergeTool.cs), [SplitTool](/Core/Ypdf.Core/Tools/SplitTool.cs), or [CheckCompressionCapabilityTool](/Core/Ypdf.Core/Tools/CheckCompressionCapabilityTool.cs).
