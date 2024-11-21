from PIL import Image

# Create a blank image
image = Image.new('RGB', (100, 100), color='blue')
image.save('test_image.jpg')

print("Test image created successfully as 'test_image.jpg'")