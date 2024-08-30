"""
This module provides the inference function to apply style transfer to an image using a
pre-trained neural network.

The `inference` function loads a specified model and applies it to a given image, resizing the image 
and then transforming it according to the style defined by the model.
"""
import config
import cv2

def inference(model, image):
    """
    Apply style transfer to an image using a specified model.

    Args:
        model (str): The name of the model (without the file extension) to be used for style transfer.
        image (numpy.ndarray): The input image as a numpy array.

    Returns:
        output (numpy.ndarray): The stylized output image.
        resized_image (numpy.ndarray): The resized version of the input image.
    """
    try:
        model_name = f"{config.MODEL_PATH.rstrip('/')}/{model}.t7"
        model = cv2.dnn.readNetFromTorch(model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to load model {model_name}: {e}") from e

    height, width = int(image.shape[0]), int(image.shape[1])
    new_width = int((640 / height) * width)
    resized_image = cv2.resize(image, (new_width, 640), interpolation=cv2.INTER_AREA)

    # Create our blob from the Image
    # Then perform a forward pass run of the network
    # the mean values for the ImageNet training set are R=103.93, G=116.77, B=123.68

    inp_blob = cv2.dnn.blobFromImage(
        resized_image,
        1.0,
        (new_width, 640),
        (103.93, 116.77, 123.68),
        swapRB=False,
        crop=False,
    )

    model.setInput(inp_blob)
    output = model.forward()

    # Reshape the output Tensor,
    # add back the mean substraction
    # re-order the channels
    output = output.reshape(3, output.shape[2], output.shape[3])
    output[0] += 103.93
    output[1] += 116.77
    output[2] += 123.68

    output = output.transpose(1, 2, 0)

    return output, resized_image
