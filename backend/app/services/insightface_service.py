import insightface
import numpy as np

class InsightfaceService:
    def __init__(self):
        self.app = insightface.app.FaceAnalysis(name='buffalo_l', providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def detect(self, image):
        detected_face = self.app.get(image)
        return detected_face

    def analyze(self, face, list_faces):
        max_similarity = -1.0
        detected_face = None
        threshold = 0.4

        for stored_face in list_faces:
            dot_product = np.dot(face.embedding, stored_face.embedding)
            norm_a = np.linalg.norm(face.embedding)
            norm_b = np.linalg.norm(stored_face.embedding)
            similarity = dot_product / (norm_a * norm_b)

            if similarity > max_similarity:
                max_similarity = similarity
                detected_face = stored_face

        return detected_face if max_similarity > threshold else None