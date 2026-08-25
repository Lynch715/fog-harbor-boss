import AppKit
import Foundation
import Vision

guard CommandLine.arguments.count == 2 else {
    fputs("usage: swift verify_qr.swift <image>\n", stderr)
    exit(2)
}

let imagePath = CommandLine.arguments[1]
guard
    let image = NSImage(contentsOfFile: imagePath),
    let tiff = image.tiffRepresentation,
    let bitmap = NSBitmapImageRep(data: tiff),
    let cgImage = bitmap.cgImage
else {
    fputs("cannot open image\n", stderr)
    exit(3)
}

let request = VNDetectBarcodesRequest()
request.symbologies = [.qr]
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

do {
    try handler.perform([request])
    let payloads = request.results?.compactMap(\.payloadStringValue) ?? []
    if payloads.isEmpty {
        fputs("no QR code detected\n", stderr)
        exit(4)
    }
    payloads.forEach { print($0) }
} catch {
    fputs("Vision error: \(error)\n", stderr)
    exit(5)
}
