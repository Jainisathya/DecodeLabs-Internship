from torchvision import models
from torchvision import transforms
from PIL import Image
import torch

# Load pretrained model
weights = models.ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights)
model.eval()

labels = weights.meta["categories"]

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

def classify_image(image: Image.Image):

    image = image.convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    top5 = torch.topk(probabilities, 5)

    predictions = []

    for score, index in zip(top5.values, top5.indices):

        predictions.append(
            {
                "label": labels[index.item()],
                "confidence": float(score.item() * 100)
            }
        )

    return predictions