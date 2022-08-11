# QRCode_Scanner

Lenor

## Working

Automatically fix and recognize QR code pictures taken from different angles.

## Usage

Copy this folder to your project root.

import this folder as a module by

```python
import qrcode_scanner
```

And then using (image is a OpenCV mat image)

```Python
qrcode_scanner.decode_qrcode(image)
```

ret is a string.

Notice that if there's multiple qrcode in the image, only the first one will be recognized.