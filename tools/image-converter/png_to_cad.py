import cv2
import ezdxf
import numpy as np
import argparse
import os
import sys

def png_to_dxf(input_path, output_path, threshold=127, blur=0, epsilon=0.001, scale=1.0, invert=False, use_splines=False, debug=False, smooth=0):
    """
    Converts a PNG image to a DXF vector file with morphological smoothing for professional outlines.
    """
    # 1. Load image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image {input_path}")
        return

    # 2. Pre-process
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if blur > 0:
        if blur % 2 == 0:
            blur += 1
        gray = cv2.GaussianBlur(gray, (blur, blur), 0)

    if invert:
        gray = cv2.bitwise_not(gray)

    # 3. Thresholding Logic
    if threshold == -1:
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        mode_desc = "Otsu"
    elif threshold == -2:
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 21, 2)
        mode_desc = "Adaptive"
    else:
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        mode_desc = f"Fixed({threshold})"

    # 4. Morphological Smoothing [NEW]
    # This cleans up jagged "staircase" pixel edges before tracing
    if smooth > 0:
        kernel = np.ones((smooth, smooth), np.uint8)
        # Opening removes small noise; Closing fills small holes; 
        # Combined they smooth out the jittery outlines of raster pixels.
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        mode_desc += f" + Smooth({smooth}px)"

    if debug:
        debug_path = os.path.splitext(output_path)[0] + "_debug.png"
        cv2.imwrite(debug_path, thresh)
        print(f"Debug image saved to {debug_path}")

    # 5. Find Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)

    # 6. Create DXF Document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    height, width = thresh.shape

    # 7. Add Contours to DXF
    added_count = 0
    for contour in contours:
        if len(contour) < 3:
            continue
            
        # Simplify contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon * peri, True)
        
        # Convert points to CAD coordinates
        points = []
        for pt in approx:
            x = float(pt[0][0] * scale)
            y = float((height - pt[0][1]) * scale)
            points.append((x, y))

        if len(points) < 3:
            continue

        if use_splines:
            pts = points + [points[0]]
            msp.add_spline(pts, degree=3)
        else:
            msp.add_lwpolyline(points, close=True)
        added_count += 1

    # 8. Save
    doc.saveas(output_path)
    print(f"Successfully converted {input_path} to {output_path}")
    print(f"Mode: {mode_desc}, Contours found: {len(contours)}, Contours added: {added_count}")

def main():
    parser = argparse.ArgumentParser(description="Professional PNG to DXF vector converter.")
    parser.add_argument("input", help="Path to input PNG image")
    parser.add_argument("-o", "--output", help="Path to output DXF file")
    parser.add_argument("-t", "--threshold", type=int, default=127, help="Threshold. (0-255, -1 for Otsu, -2 for Adaptive). Default: 127")
    parser.add_argument("-b", "--blur", type=int, default=0, help="Gaussian blur size. Default: 0")
    parser.add_argument("-e", "--epsilon", type=float, default=0.001, help="Simplification factor. Default: 0.001")
    parser.add_argument("-s", "--scale", type=float, default=1.0, help="Scale factor. Default: 1.0")
    parser.add_argument("-i", "--invert", action="store_true", help="Invert image")
    parser.add_argument("--spline", action="store_true", help="Output using Spline entities")
    parser.add_argument("--debug", action="store_true", help="Save binarized intermediate image")
    parser.add_argument("--smooth", type=int, default=0, help="Morphological smoothing kernel size (e.g., 3). Removes wobbly edges.")

    args = parser.parse_args()

    if not args.output:
        base = os.path.splitext(args.input)[0]
        args.output = base + ".dxf"

    png_to_dxf(
        args.input, 
        args.output, 
        threshold=args.threshold, 
        blur=args.blur, 
        epsilon=args.epsilon, 
        scale=args.scale, 
        invert=args.invert,
        use_splines=args.spline,
        debug=args.debug,
        smooth=args.smooth
    )

if __name__ == "__main__":
    main()
