# Importing necessary libraries
import gradio as gr  # Gradio library to create web-based interfaces
from transformers import BlipProcessor, BlipForConditionalGeneration  # BLIP model classes for image captioning
from PIL import Image  # PIL library to handle image input and processing

# Loading the BLIP processor and model for image captioning from pre-trained weights
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")  # Processor to prepare input data
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")  # Model to generate captions

def generate_caption(image):
    """
    Generates a caption for a given image using the BLIP model.
    
    Args:
        image: A PIL Image object to generate a caption for.

    Returns:
        caption: A text string representing the generated caption.
    """
    # Process the input image and convert it into tensors for the model
    inputs = processor(images=image, return_tensors="pt")  # "pt" denotes PyTorch tensors
    # Generate caption based on the processed inputs
    outputs = model.generate(**inputs)
    # Decode the model's output into a human-readable text
    caption = processor.decode(outputs[0], skip_special_tokens=True)  # Skipping special tokens for clean output
    return caption  # Return the generated caption

def caption_image(image):
    """
    A wrapper function that calls generate_caption and handles exceptions.
    
    Args:
        image: A PIL Image object for which a caption is required.

    Returns:
        A caption string if successful, or an error message in case of failure.
    """
    try:
        # Call the generate_caption function to get a caption for the image
        caption = generate_caption(image)
        return caption  # Return the generated caption
    except Exception as e:
        # Handle any errors that occur during caption generation
        return f"An error occurred: {str(e)}"

# Setting up a Gradio interface for the captioning application
iface = gr.Interface(
    fn=caption_image,  # The function to be called when an image is uploaded
    inputs=gr.Image(type="pil"),  # Input type as an image processed by PIL
    outputs="text",  # Output will be displayed as text
    title="Image Captioning with BLIP",  # Title of the web interface
    description="Upload an image to generate a caption."  # A brief description of the interface's purpose
)

# Launch the Gradio interface in a web browser
iface.launch()
