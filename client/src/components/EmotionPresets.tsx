import React from 'react';
import { useMainStore } from '../hooks/useMainStore';
import { useFacePokeAPI } from '../hooks/useFacePokeAPI';

import { ActionMode, ClosestLandmark, LandmarkGroup } from '../types';

interface EmotionPreset {
  name: string;
  landmarks: Array<{
    group: LandmarkGroup;
    vector: { x: number; y: number; z: number };
    aaa?: number;
    eee?: number;
    eyebrow?: number;
    eyes?: number;
    pupil_x?: number;
    pupil_y?: number;
    rotate_pitch?: number;
    rotate_roll?: number;
    rotate_yaw?: number;
  }>;
  description?: string;
}

const EMOTION_PRESETS: EmotionPreset[] = [
  {
    name: "😠 Angry",
    landmarks: [
      {
        // A slight downward tilt can emphasize the aggressive stance.
        group: "background",
        vector: { x: 0.12, y: -0.04, z: 0 },  // y positive for downward pitch
      },
      {
        // Furrowed, lowered eyebrows.
        group: "leftEyebrow",
        vector: { x: 0.05, y: 0.15, z: 0 },
        eyebrow: -1.29,
      },
      {
        // Narrowed eyes.
        group: "leftEye",
        vector: { x: 0.18, y: -0.25, z: 0 },
        eyes: -1.08,
        pupil_x: 5.5,
        pupil_y: 0,
      },
      {
        // A tense, downturned mouth.
        group: "lips",
        vector: { x: -0.38, y: 0.36, z: 0 },
        aaa: -10.08,
        eee: -16.02,
      },
    ],
    description: "Furrowed eyebrows, narrowed eyes, and a tense, downturned mouth",
  },
  {
    name: "😢 Sad",
    landmarks: [
      {
        // A slight head drop to emphasize a sorrowful look.
        group: "background",
        vector: {
          x: -0.11, y: 0.12, z: 0,
        },  // y positive for downward pitch
      },
      {
        // Softly raised eyebrows to give a plaintive look.
        group: "leftEyebrow",
        vector: { x: 0.01, y: 0.16, z: 0 },
        eyebrow: -1.68,
      },
      {
        // Slightly drooping eyes.
        group: "leftEye",
        vector: { x: -0.2334098950897014,y: 0.11482211814970011, z: 0},
        eyes: -10,
        pupil_x: -7,
      },
      {
        // A downturned mouth.
        group: "lips",
        vector: { x: 0, y: 0.47, z: 0 },
        aaa: -26,
        eee: -2,
      },
    ],
    description: "Drooping features with a downturned mouth",
  },
  {
    name: "😮 Surprised",
    landmarks: [
      {
        // A slight head tilt backward and to the side.
        group: "background",
        vector: { x: -0.03, y: 0.06, z: 0 },  // x negative for positive yaw, y negative for upward pitch
      },
      {
        // Moderately raised eyebrows.
        group: "leftEyebrow",
        vector: { x: 0.05, y: -0.48, z: 0 },
        eyebrow: 14.70,
      },
      {
        // Eyes wide open with slightly shifted pupils.
        group: "leftEye",
        vector: { x: 0.01, y: -0.43, z: 0 },
        eyes: 3.5,
        pupil_x: 0.56,
        pupil_y: 0,
      },
      {
        // A mouth that’s partly open but tense.
        group: "lips",
        vector: { x: 0.02, y: -0.41, z: 0 },
        aaa: 107,
        eee: -1.76,
      },
    ],
    description: "Raised eyebrows, wide open eyes, and an open mouth",
  },
  {
    name: "🤔 Thinking",
    landmarks: [
      {
        // A relaxed head posture with a thoughtful tilt.
        group: "background",
        vector: { x: 0.5, y: -0.3, z: 0 },  // x positive for negative yaw, y negative for upward pitch
      },
      {
        // A slightly raised eyebrow hinting at concentration.
        group: "leftEyebrow",
        vector: { x: 0.12, y: -0.42, z: 0 },
        eyebrow: 13.03,
      },
      {
        // A slight, ambiguous smirk.
        group: "lips",
        vector: { x: -0.09, y: 0.31, z: 0 },
        aaa: -1.52,
        eee: -5.89,
      },
    ],
    description: "A contemplative look with a subtle head tilt and smirk",
  },
  {
    name: "😊 Happy",
    landmarks: [
      {
        // A slight upward tilt for a cheerful look.
        group: "background",
        vector: { x: 0.1, y: -0.1, z: 0 },  // x positive for negative yaw, y negative for upward pitch
      },
      {
        // Softly raised eyebrows that contribute to a joyful expression.
        group: "leftEyebrow",
        vector: { x: 0.54, y:-0.45, z: 0 },
        eyebrow: 13,
      },
      {
        group: "rightEyebrow",
        vector: { x: 0.54, y:-0.45, z: 0 },
        eyebrow: 13,
      },
      {
        // Eyes that are gently open.
        group: "leftEye",
        vector: { x: 0.045, y: -0.39, z: 0 },
        eyes: 2.5,
      },
      {
        // A broad, uplifting smile.
        group: "lips",
        vector: { x: 0.41, y: 0.21, z: 0 },
        aaa: 13,
        eee: 12,
      },
    ],
    description: "A broad smile with relaxed, cheerful features",
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
              emotion.landmarks.forEach((landmark) => {
                const { group, vector, ...params } = landmark;
                modifyImage({
                  landmark: {
                    group,
                    distance: Math.sqrt(vector.x * vector.x + vector.y * vector.y),
                    vector,
                    ...params
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
