// ============================================
// MongoDB Initialization Script
// Hot Wheels Platform - Media Database
// ============================================

print('🚀 Initializing MongoDB for Hot Wheels Platform...');

// Switch to application database
db = db.getSiblingDB('hotwheels_media');

// Create application user
db.createUser({
  user: 'hotwheels_app',
  pwd: 'app_mongo_pass_123',
  roles: [
    { role: 'readWrite', db: 'hotwheels_media' },
    { role: 'dbAdmin', db: 'hotwheels_media' }
  ]
});

print('✓ Application user created');

// Create collections
db.createCollection('model_media');
db.createCollection('user_uploads');
db.createCollection('image_metadata');

print('✓ Collections created');

// Create indexes for model_media
db.model_media.createIndex({ model_id: 1 });
db.model_media.createIndex({ "images.type": 1 });
db.model_media.createIndex({ "images.uploaded_at": -1 });
db.model_media.createIndex({ model_id: 1, "images.type": 1 });

print('✓ Indexes for model_media created');

// Create indexes for user_uploads
db.user_uploads.createIndex({ user_id: 1 });
db.user_uploads.createIndex({ upload_date: -1 });
db.user_uploads.createIndex({ status: 1 });

print('✓ Indexes for user_uploads created');

// Insert sample data
db.model_media.insertOne({
  model_id: 1,
  casting_name: "Nissan Skyline GT-R (R34)",
  images: [
    {
      url: "https://images.hotwheels.com/2025/skyline-gtr-r34-blue-front.jpg",
      type: "product",
      dimensions: { width: 1920, height: 1080 },
      file_size: 245678,
      format: "jpeg",
      uploaded_at: new Date("2025-01-10T10:00:00Z"),
      uploaded_by: 9,
      is_primary: true
    }
  ],
  videos: [],
  metadata: {
    color_profile: "sRGB",
    has_transparency: false,
    dominant_colors: ["#0052A3", "#FFFFFF", "#000000"]
  },
  created_at: new Date(),
  updated_at: new Date()
});

print('✓ Sample data inserted');

// Validation schema (optional but recommended)
db.runCommand({
  collMod: "model_media",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["model_id"],
      properties: {
        model_id: {
          bsonType: "int",
          description: "Reference to PostgreSQL car_models.model_id"
        },
        casting_name: {
          bsonType: "string"
        },
        images: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["url", "type"],
            properties: {
              url: { bsonType: "string" },
              type: { enum: ["product", "packaging", "detail", "user_photo"] },
              dimensions: {
                bsonType: "object",
                properties: {
                  width: { bsonType: "int" },
                  height: { bsonType: "int" }
                }
              }
            }
          }
        }
      }
    }
  },
  validationLevel: "moderate"
});

print('✓ Validation schema applied');
print('✅ MongoDB initialization completed!');
