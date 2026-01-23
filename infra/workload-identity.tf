                                                                                                                      
  # -----------------------------------------------------------------------------                                      
  # Workload Identity Federation - Keyless auth for GitHub Actions                                                     
  # -----------------------------------------------------------------------------                                      
                                                                                                                       
  resource "google_iam_workload_identity_pool" "github_pool" {                                                         
    workload_identity_pool_id = "github-pool"                                                                          
    display_name              = "GitHub Actions Pool"                                                                  
    description               = "Identity pool for GitHub Actions OIDC"                                                
    disabled                  = false                                                                                  
  }           


   resource "google_iam_workload_identity_pool_provider" "github_provider" {                           
    workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id                             
    workload_identity_pool_provider_id = "github-provider"                                            
    display_name                       = "GitHub Actions Provider"                                    
                                                                                                      
    attribute_mapping = {                                                                             
      "google.subject"       = "assertion.sub"                                                        
      "attribute.actor"      = "assertion.actor"                                                      
      "attribute.repository" = "assertion.repository"                                                 
    }                                                                                                 
                                                                                                      
    # Only allow your specific repo                                                                   
    attribute_condition = "assertion.repository == \"lucien95/Remote-vitals-streaming\""              
                                                                                                      
    oidc {                                                                                            
      issuer_uri = "https://token.actions.githubusercontent.com"                                      
    }                                                                                                 
  }                                                                                                           
                                                                                                                       