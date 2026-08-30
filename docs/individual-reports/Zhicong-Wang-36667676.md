# Individual Report: Zhicong Wang

**Student ID:** 36667676  
**Team:** Group 13  
**Assigned area:** Member 04 - infrastructure and deployment

## Role and contribution

I was responsible for infrastructure and deployment. I worked on the Terraform definition for the AWS and Alibaba Cloud boundary, including Cognito, API Gateway JWT authorization, private S3 prefixes, DynamoDB, SQS with a dead-letter queue, Lambda roles, SNS notifications and the Function Compute worker configuration. I focused on least-privilege permissions and on keeping secrets, Terraform state, model weights and local environment files out of source control. I also investigated deployment failures and recorded the Terraform remote-state network timeout repair using the reachable dual-stack S3 endpoint. I verified the deployed regions, service endpoints, image digests, worker execution role, OSS read policy and SLS logging configuration. The deployment, security-scan, remote-state and cloud-evidence records are preserved in `docs/evidence` and the Terraform runbook.

I also checked that the production configuration uses digest-pinned images and that the worker receives model access through its Alibaba execution role rather than embedded credentials. The Terraform definitions separate public API entry points from private storage prefixes and use a redrive policy for failed processing messages. I recorded both successful checks and unresolved risks, including the upstream image findings and historical DLQ messages, so the final report does not overstate the deployment's security posture.

## Teamwork reflection

Infrastructure work made the coupling between all four areas visible. A small permission or timeout issue could appear as an application failure, so I found it important to compare the Terraform plan, cloud console state and application response before changing anything. The team communicated effectively when we treated each failure as evidence and recorded the exact repair, such as adding a missing DynamoDB permission or extending the worker health-check delay. We also preserved deletion and restoration evidence instead of hiding the destructive test. Our main improvement would be to reserve a final deployment rehearsal with a clean account session, because vulnerability findings, DLQ messages and account-specific configuration still require explicit review before submission.

This experience reinforced that infrastructure evidence should be collected at the same time as application evidence. A console screenshot without the corresponding plan or request result is difficult to interpret, while the three together explain what changed and why. For future work I would schedule a final freeze window in which Terraform, cloud consoles, logs and the demo script are reviewed against one versioned checklist.

## Generative AI declaration

GPT was used only to brainstorm design options and to help debug implementation errors. I reviewed every suggestion, tested the resulting system, and can explain, modify and defend my submitted work.
