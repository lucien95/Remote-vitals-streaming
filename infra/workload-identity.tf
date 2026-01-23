                                                                                                                      
  # -----------------------------------------------------------------------------                                      
  # Workload Identity Federation - Keyless auth for GitHub Actions                                                     
  # -----------------------------------------------------------------------------                                      
                                                                                                                       
  resource "google_iam_workload_identity_pool" "github_pool" {                                                         
    workload_identity_pool_id = "github-pool"                                                                          
    display_name              = "GitHub Actions Pool"                                                                  
    description               = "Identity pool for GitHub Actions OIDC"                                                
    disabled                  = false                                                                                  
  }                                                                                                                    
                                                                                                                       