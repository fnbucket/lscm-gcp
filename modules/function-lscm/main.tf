# provider "google" {
#   credentials = file("~/key.json")
#   project     = "lscm-2233"
#   region      = "us-central1"
#   zone        = "us-central1-a"
# }

# zip up our source code
data "archive_file" "lscm_zip" {
 type        = "zip"
 source_dir  = "../../src/lscm/"
 output_path = "../../src/lscm.zip"
}

# create the storage bucket
resource "google_storage_bucket" "lscm_bucket" {
 name   = "lscm-fn-bucket"
}

# place the zip-ed code in the bucket
resource "google_storage_bucket_object" "lscm_zip" {
 name   = "lscm.zip"
 bucket = "${google_storage_bucket.lscm_bucket.name}"
 source = "../../src/lscm.zip"
}

resource "google_cloudfunctions_function" "function" {
 name                  = "lscm-fn-bucket"
 description           = "lscm function implements: http://rosalind.info/problems/lcsm/"
 available_memory_mb   = 256
 source_archive_bucket = "${google_storage_bucket.lscm_bucket.name}"
 source_archive_object = "${google_storage_bucket_object.lscm_zip.name}"
 timeout               = 60
 entry_point           = "lscm"
 trigger_http          = true
 runtime               = "python37"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
