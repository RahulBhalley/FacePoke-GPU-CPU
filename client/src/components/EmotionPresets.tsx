import React from 'react';
import { useMainStore } from '../hooks/useMainStore';
import { useFacePokeAPI } from '../hooks/useFacePokeAPI';

import { ActionMode, ClosestLandmark, LandmarkGroup } from '../types';

interface EmotionPreset {
  name: string;
  landmarks: Array<{
    group: LandmarkGroup;
    vector: { x: number; y: number; z: number };
  }>;
  description?: string;
}

const EMOTION_PRESETS: EmotionPreset[] = [
  { 
    name: "😠 Angry", 
    landmarks: [
      { group: 'background', vector: { x: 0, y: 0.3, z: 0 } },      // tilt head down
      { group: 'leftEyebrow', vector: { x: 0, y: 0.3, z: 0 } },     // furrow brows
      { group: 'rightEyebrow', vector: { x: 0, y: 0.3, z: 0 } },    // furrow brows
      { group: 'leftEye', vector: { x: 0, y: 0.3, z: 0 } },         // squint eyes
      { group: 'rightEye', vector: { x: 0, y: 0.3, z: 0 } },        // squint eyes
      { group: 'lips', vector: { x: 0, y: 0.3, z: 0 } }             // frown
    ],
    description: "Tilted down, intense gaze" 
  },
  { 
    name: "😢 Sad", 
    landmarks: [
      { group: 'background', vector: { x: 0, y: 0.3, z: 0 } },      // tilt head down
      { group: 'leftEyebrow', vector: { x: 0, y: -0.3, z: 0 } },    // raise inner brows
      { group: 'rightEyebrow', vector: { x: 0, y: -0.3, z: 0 } },   // raise inner brows
      { group: 'lips', vector: { x: 0, y: 0.3, z: 0 } }             // frown
    ],
    description: "Looking down, slight tilt" 
  },
  { 
    name: "😮 Surprised", 
    landmarks: [
      { group: 'background', vector: { x: 0, y: -0.3, z: 0 } },     // tilt head up
      { group: 'leftEyebrow', vector: { x: 0, y: -0.4, z: 0 } },    // raise brows
      { group: 'rightEyebrow', vector: { x: 0, y: -0.4, z: 0 } },   // raise brows
      { group: 'leftEye', vector: { x: 0, y: -0.3, z: 0 } },        // widen eyes
      { group: 'rightEye', vector: { x: 0, y: -0.3, z: 0 } },       // widen eyes
      { group: 'lips', vector: { x: 0, y: -0.4, z: 0 } }            // open mouth
    ],
    description: "Looking up, wide-eyed" 
  },
  { 
    name: "😨 Scared", 
    landmarks: [
      { group: 'background', vector: { x: 0.2, y: -0.3, z: 0 } },   // tilt head back and side
      { group: 'leftEyebrow', vector: { x: 0, y: -0.4, z: 0 } },    // raise brows
      { group: 'rightEyebrow', vector: { x: 0, y: -0.4, z: 0 } },   // raise brows
      { group: 'leftEye', vector: { x: 0, y: -0.3, z: 0 } },        // widen eyes
      { group: 'rightEye', vector: { x: 0, y: -0.3, z: 0 } },       // widen eyes
      { group: 'lips', vector: { x: 0, y: -0.3, z: 0 } }            // open mouth
    ],
    description: "Tilted back, fearful expression" 
  },
  { 
    name: "🤔 Thinking", 
    landmarks: [
      { group: 'faceOval', vector: { x: 0.3, y: 0, z: 0 } },       // tilt head sideways
      { group: 'leftEyebrow', vector: { x: 0, y: -0.2, z: 0 } },    // raise one brow
      { group: 'lips', vector: { x: 0.2, y: 0, z: 0 } }            // purse lips
    ],
    description: "Tilted, contemplative look" 
  },
  { 
    name: "😊 Happy", 
    landmarks: [
      { group: 'background', vector: { x: 0, y: -0.1, z: 0 } },     // slight head up
      { group: 'leftEyebrow', vector: { x: 0, y: -0.2, z: 0 } },    // raise brows
      { group: 'rightEyebrow', vector: { x: 0, y: -0.2, z: 0 } },   // raise brows
      { group: 'leftEye', vector: { x: 0, y: 0.2, z: 0 } },         // squint eyes
      { group: 'rightEye', vector: { x: 0, y: 0.2, z: 0 } },        // squint eyes
      { group: 'lips', vector: { x: 0.3, y: -0.2, z: 0 } }          // wide smile
    ],
    description: "Cheerful expression" 
  },
];

export function EmotionPresets() {
  const { modifyImage } = useMainStore();
  const previewImage = useMainStore(s => s.previewImage);

  if (!previewImage) return null;

  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold mb-2">Emotion Presets</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
        {EMOTION_PRESETS.map((emotion) => (
          <button
            key={emotion.name}
            onClick={() => {
              // Apply each landmark modification in sequence
              emotion.landmarks.forEach(({ group, vector }) => {
                modifyImage({
                  landmark: {
                    group,
                    distance: Math.sqrt(vector.x * vector.x + vector.y * vector.y),
                    vector
                  },
                  vector,
                  mode: 'PRIMARY' as ActionMode
                });
              });
            }}
            className="px-3 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-md text-sm transition-colors"
            title={emotion.description}
          >
            {emotion.name}
          </button>
        ))}
      </div>
    </div>
  );
}
