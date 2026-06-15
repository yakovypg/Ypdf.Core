using System;
using Ypdf.Core.Utils;

namespace Ypdf.Core.Imaging;

public readonly struct ImageRendering : IEquatable<ImageRendering>
{
    private const int _defaultDpi = 150;
    private const string _defaultExtension = "png";

    public ImageRendering()
        : this(_defaultDpi, _defaultExtension) { }

    public ImageRendering(int dpi, string extension = _defaultExtension)
    {
        DefaultExceptions.ThrowIfNegativeOrZero(dpi, nameof(dpi));
        ExtendedArgumentException.ThrowIfNullOrWhiteSpace(extension, nameof(extension));

        Dpi = dpi;
        Extension = extension;
    }

    public readonly int Dpi { get; }
    public readonly string Extension { get; }

    public static bool operator ==(ImageRendering left, ImageRendering right)
    {
        return left.Equals(right);
    }

    public static bool operator !=(ImageRendering left, ImageRendering right)
    {
        return !(left == right);
    }

    public bool Equals(ImageRendering other)
    {
        return Dpi == other.Dpi && Extension == other.Extension;
    }

    public override bool Equals(object? obj)
    {
        return obj is ImageRendering other
            && Equals(other);
    }

    public override int GetHashCode()
    {
        return HashGenerator.Generate(Dpi, Extension);
    }
}
