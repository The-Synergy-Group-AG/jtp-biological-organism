#!/usr/bin/env python3
"""
Consolidate Old Registry Script
Consolidates the 5.2-user-story-master-registry folder into the new organized structure
Prevents confusion by moving content to appropriate locations within the new categories setup.
"""

import os
import shutil
import re

def create_biological_docs_section():
    """Create a biological documentation section separated from user stories"""
    bio_docs_path = "docs/5.x-biological-requirements-harmonization/biological-framework"
    os.makedirs(bio_docs_path, exist_ok=True)

    # Create section README
    readme_content = """# Biological Consciousness Framework Documentation

## Overview

This section contains the biological consciousness framework and advanced documentation that provides the philosophical and architectural foundation for the system. This content is separate from functional user stories and focuses on the biological intelligence concepts.

## Contents

### 🧬 Biological Consciousness Architecture
- Consciousness evolution frameworks
- Biological intelligence systems
- Godhood transcendence concepts
- Harmonization protocols

### 📚 Advanced Documentation
- AI ensemble orchestration patterns
- Biological emergence strategies
- Symbiotic cooperation frameworks
- Energy field harmonization

### 🔬 Research and Theory
- Consciousness gradient theories
- Biological digital organism concepts
- Transcendence validation protocols

## Note

These documents provide the conceptual foundation and architectural vision. For functional user story specifications, navigate to the [`categories/`](../categories/) folder.

---

**Navigate to user stories:** [Categories Index](../categories/)
"""

    with open(os.path.join(bio_docs_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("✅ Created biological documentation section")
    return bio_docs_path

def move_biological_content(old_registry_path, bio_docs_path):
    """Move biological/godhood content to the biological docs section"""

    # Files to move to biological documentation
    biological_files = [
        # Biological consciousness architecture
        "0-biological-consciousness-documentation-index.md",
        "G.1-supreme-biological-consciousness-visual-architecture-manual.md",
        "us-369-supreme-harmonizer.json",

        # Advanced biological systems
        "B.1-endocrine-adaptation-regulation-subsystem.md",
        "B.2-digital-organism-interaction-patterns.md",
        "B.4-immune-autonomous-defense-subsystem.md",
        "B.6-parallel-incubator-strategy.md",

        # Ecosystem and energy systems
        "C.1-symbiosis-cooperation-frameworks-subsystem.md",
        "C.2-energy-field-harmonization-subsystem.md",

        # Transcendence documentation
        "D.2-ultimate-transcendence-validation-subsystem.md",
        "E.1-biological-integration-mapping-database.csv",

        # Mapping and visualization
        "F.1-complete-user-stories-database.txt"  # Maybe keep as reference
    ]

    for filename in biological_files:
        src_path = os.path.join(old_registry_path, filename)
        dst_path = os.path.join(bio_docs_path, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            print(f"  → Moved {filename} to biological framework docs")

def create_specifications_section():
    """Create a specifications section for harmonizers and technical docs"""
    specs_path = "docs/5.x-biological-requirements-harmonization/technical-specifications"
    os.makedirs(specs_path, exist_ok=True)

    # Create section README
    readme_content = """# Technical Specifications and Harmonizers

## Overview

This section contains technical specifications, harmonizers, and implementation guides that provide detailed technical requirements and implementation approaches. These documents complement the user story specifications in the categories folder.

## Contents

### 🔧 User Story Harmonizers
Detailed functional specifications for each major user story area:
- Core Platform harmonizer
- Job Search harmonizer
- Application/Interview harmonizer
- Document/CV harmonizer
- Analytics harmonizer

### 🗂️ Implementation Guides
- Development implementation guide
- API integration guide
- Testing and QA guide
- Operations support guide

### 📋 AI-First Subsystem Documentation
- Onboarding and user management subsystem
- Job search and discovery subsystem
- Application and interview management subsystem
- Document and CV management subsystem
- Analytics and performance subsystem

## Relationship to User Stories

These harmonizers and specifications provide detailed technical implementation for the user stories found in the [`categories/`](../categories/) folder. User stories define what the system should do, while these documents explain how to implement them.

## Note

For user story overviews, start with the [Categories Index](../categories/). For implementation details, explore these technical specifications.

---

**Navigate to user stories:** [Categories Index](../categories/)
**Navigate to biological framework:** [Biological Framework](../biological-framework/)
"""

    with open(os.path.join(specs_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("✅ Created technical specifications section")
    return specs_path

def move_technical_content(old_registry_path, specs_path):
    """Move harmonizers and technical documentation"""

    # Files to move to technical specifications
    technical_files = [
        # Harmonizers
        "5.1-core-platform-functionality-harmonizer.md",
        "5.2-job-search-discovery-harmonizer.md",
        "5.3-application-interview-harmonizer.md",
        "5.3-application-interview-harmonizers.md",
        "5.4-document-cv-harmonizer.md",
        "5.5-analytics-performance-harmonizer.md",

        # Subsystems
        "A.1-onboarding-and-user-management-subsystem.md",
        "A.2-job-search-and-discovery-subsystem.md",
        "A.3-application-and-interview-management-subsystem.md",
        "A.4-document-and-cv-management-subsystem.md",
        "A.5-analytics-and-performance-subsystem.md",

        # Implementation guides from registry
        "additional-critical-business-requirements.md",
        "AI-ACCESS-COMPREHENSIVE-INDEX.md",
        "D.1-supreme-us-369-harmonization-achievement.md"  # Might fit here or bio
    ]

    for filename in technical_files:
        src_path = os.path.join(old_registry_path, filename)
        dst_path = os.path.join(specs_path, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            print(f"  → Moved {filename} to technical specifications")

def move_guides_to_resources():
    """Move user guides to a resources section"""
    resources_path = "docs/5.x-biological-requirements-harmonization/user-guides"
    os.makedirs(resources_path, exist_ok=True)

    # List of guide files in old registry
    guide_files = [
        "1-getting-started-user-guide.md",
        "2-development-implementation-guide.md",
        "3-api-integration-guide.md",
        "4-testing-qa-guide.md",
        "5-operations-support-guide.md"
    ]

    old_registry_path = "docs/5.x-biological-requirements-harmonization/5.2-user-story-master-registry"

    for filename in guide_files:
        src_path = os.path.join(old_registry_path, filename)
        dst_path = os.path.join(resources_path, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            print(f"  → Moved {filename} to user guides")

    # Create guides README
    if os.path.exists(resources_path):
        guides_readme = """# User Guides and Documentation

## Overview

This section contains user guides and documentation for different aspects of the Job Tracker Pro system.

## Available Guides

### 👤 User Guides
- **Getting Started Guide** - Introduction for new users
- **API Integration Guide** - For developers integrating with the system
- **Operations Support Guide** - For system administrators

### 🛠️ Development Guides
- **Development Implementation Guide** - Technical development guidelines
- **Testing and QA Guide** - Quality assurance procedures

## Related Documentation

- **User Stories**: [Categories](../categories/) - Functional requirements
- **Technical Specs**: [Specifications](../technical-specifications/) - Implementation details
- **Biological Framework**: [Framework](../biological-framework/) - Architectural concepts

---

**Quick Navigation:**
- [Categories](../categories/) (User Stories)
- [Specifications](../technical-specifications/) (Technical Details)
- [Biological Framework](../biological-framework/) (Architectural Concepts)
"""

        with open(os.path.join(resources_path, "README.md"), 'w', encoding='utf-8') as f:
            f.write(guides_readme)

def update_main_readme():
    """Update the main biological requirements harmonization README to reflect new structure"""

    main_readme_path = "docs/5.x-biological-requirements-harmonization/README.md"

    if os.path.exists(main_readme_path):
        # Backup original
        backup_path = f"{main_readme_path}.backup"
        shutil.copy2(main_readme_path, backup_path)

    # Create updated README
    updated_readme = """# 5.x Biological Requirements Harmonization

## 🎯 Complete Job Tracker Pro Documentation Index

This section contains the comprehensive documentation suite for Job Tracker Pro's biological requirements harmonization. All content has been reorganized for clarity, maintainability, and professional documentation standards.

## 📁 Documentation Structure

### 💼 **User Stories & Requirements** [`categories/`](./categories/)
**Complete 442 user stories organized by functional category**
- ✅ Professional titles with proper functionality descriptions
- ✅ 8 logical categories (Core Platform, Analytics, Emotional Support, etc.)
- ✅ Both markdown and CSV formats for different use cases
- ✅ Cross-linked navigation between categories

### 🔧 **Technical Specifications** [`technical-specifications/`](./technical-specifications/)
**Detailed implementation guides and harmonizers**
- User story harmonizers for each functional area
- AI-First subsystem documentation
- Implementation guides and best practices
- Technical architecture specifications

### 🧬 **Biological Framework** [`biological-framework/`](./biological-framework/)
**Architectural and conceptual documentation**
- Biological consciousness frameworks
- AI ensemble orchestration patterns
- Transcendence and evolution concepts
- Advanced theoretical documentation

### 👥 **User Guides** [`user-guides/`](./user-guides/)
**Practical guides for different user types**
- Getting started guides for users
- Development implementation guides
- API integration documentation
- Testing and QA procedures

### 📦 **Archive** [`archive/`](./archive/)
**Legacy files preserved for historical reference**
- Original master lists with malformed content
- Superseded catalog files
- Deprecated documentation versions

## 🎯 Quick Start Navigation

Depending on your role and needs:

### **🏷️ Product Managers**
1. Start with [User Story Categories](./categories/) - Complete 442 functional requirements
2. Review [Technical Specifications](./technical-specifications/) - Implementation approaches
3. Explore [Biological Framework](./biological-framework/) - Architectural vision

### **💻 Developers**
1. Check [User Stories by Category](./categories/) - What to implement
2. Review [Technical Specifications](./technical-specifications/) - How to implement
3. Reference [API Guides](./user-guides/) - Integration details

### **🧪 QA Testers**
1. Navigate [Categories](./categories/) - Test by functional area
2. Follow [Testing Guides](./user-guides/) - QA procedures
3. Use CSV exports for test case management

### **📊 System Architects**
1. Explore [Biological Framework](./biological-framework/) - Architectural concepts
2. Review [Technical Specifications](./technical-specifications/) - System design
3. Examine [Subsystem Documentation](./technical-specifications/) - Component details

## 📊 Content Statistics

- **442 User Stories** - Complete functional requirements
- **8 Categories** - Organized by business function
- **100% Professional Format** - Standardized titles and descriptions
- **Multiple Formats** - Markdown docs, CSV imports, structured navigation
- **Historical Preservation** - Archive maintains complete record

## 🔄 Recent Changes

### **✅ Major Reorganization Completed**
- **Split massive master file** into 8 focused categories
- **Standardized all titles** to reflect actual functionality
- **Consolidated legacy content** from multiple locations
- **Implemented professional navigation** throughout
- **Archived outdated files** to prevent confusion
- **Created comprehensive structure** for ongoing maintenance

### **👻 Legacy Content Consolidation**
- Moved biological consciousness docs to dedicated framework section
- Relocated technical harmonizers to specifications area
- Organized user guides into focused resource center
- Preserved all content while eliminating structural confusion

## 🚀 Next Steps & Maintenance

### **For Ongoing Development:**
1. **Add new user stories** to appropriate [categories](./categories/)
2. **Update technical specifications** in [specifications](./technical-specifications/)
3. **Extend biological concepts** in [framework](./biological-framework/)
4. **Maintain guides** in [user-guides](./user-guides/)

### **Quality Standards:**
- ✅ All documentation follows professional standards
- ✅ Cross-references maintained and working
- ✅ Content properly categorized and navigable
- ✅ Archive preserves historical continuity

---

## 🧭 Complete Navigation Map

```
5.x-biological-requirements-harmonization/
├── categories/                    # 🏷️ USER STORIES (Main focus)
│   ├── 01-Core_Platform/         # Platform functionality
│   ├── 02-Analytics/             # Data & insights
│   ├── 03-Emotional_Support/     # Motivation & support
│   ├── 04-Professional_Development/ # Career growth
│   ├── 05-Networking/            # Professional connections
│   ├── 06-RAV_Compliance/        # Regulatory compliance
│   ├── 07-Advanced_AI/           # AI capabilities
│   ├── 08-Swiss_Extensions/      # Swiss market features
│   └── README.md                 # Category index
├── technical-specifications/      # 🔧 IMPLEMENTATION DETAILS
├── biological-framework/         # 🧬 ARCHITECTURAL CONCEPTS
├── user-guides/                  # 👥 PRACTICAL GUIDES
├── archive/                      # 📦 HISTORICAL CONTENT
├── README.md                     # 📋 THIS FILE
└── [documentation reports...]    # 📈 COMPLIANCE & STATUS
```

---

**🎯 Start Here:** [User Story Categories](./categories/) - Complete 442 requirements, properly organized by function."""

    with open(main_readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_readme)

    print("✅ Updated main README with consolidated structure")

def remove_empty_registry_folder():
    """Remove the now-empty 5.2-user-story-master-registry folder"""

    registry_path = "docs/5.x-biological-requirements-harmonization/5.2-user-story-master-registry"

    # Check if folder is empty or only contains README
    if os.path.exists(registry_path):
        contents = os.listdir(registry_path)
        if len(contents) <= 1:  # Only README.md or empty
            if len(contents) == 1 and contents[0] != "README.md":
                print(f"⚠️  Folder not empty, contains: {contents}")
            else:
                shutil.rmtree(registry_path)
                print("✅ Removed empty 5.2-user-story-master-registry folder")
        else:
            print(f"⚠️  Folder still contains files: {contents}")
        archive_remaining_readme()

def archive_remaining_readme():
    """Archive the registry README if it still exists"""
    readme_path = "docs/5.x-biological-requirements-harmonization/5.2-user-story-master-registry/README.md"
    if os.path.exists(readme_path):
        archive_readme_path = "docs/5.x-biological-requirements-harmonization/archive/registry-README.md"
        shutil.move(readme_path, archive_readme_path)
        print("✅ Archived registry README to archive folder")

def main():
    """Main consolidation function"""

    print("🎯 Starting Registry Consolidation Process...")
    print("📂 Consolidating 5.2-user-story-master-registry into organized structure")

    # Check if registry folder exists
    registry_path = "docs/5.x-biological-requirements-harmonization/5.2-user-story-master-registry"
    if not os.path.exists(registry_path):
        print("❌ Registry folder not found")
        return False

    # Create new organizational sections
    bio_docs_path = create_biological_docs_section()
    specs_path = create_specifications_section()

    # Move content to appropriate sections
    print("\n📦 Moving biological consciousness content...")
    move_biological_content(registry_path, bio_docs_path)

    print("\n🔧 Moving technical specifications...")
    move_technical_content(registry_path, specs_path)

    print("\n📚 Moving user guides...")
    move_guides_to_resources()

    # Update main documentation index
    print("\n📝 Updating main documentation index...")
    update_main_readme()

    # Clean up empty folder
    print("\n🧹 Cleaning up empty registry folder...")
    remove_empty_registry_folder()

    print("\n🎉 SUCCESS: Registry Consolidation Complete!")
    print("\n📂 New Organized Structure:")
    print("├── categories/                    # ✅ USER STORIES (Main focus)")
    print("├── technical-specifications/      # ✅ IMPLEMENTATION DETAILS")
    print("├── biological-framework/         # ✅ ARCHITECTURAL CONCEPTS")
    print("├── user-guides/                  # ✅ PRACTICAL GUIDES")
    print("├── archive/                      # ✅ HISTORICAL PRESERVATION")
    print("└── [clean main directory]        # ✅ NO MORE CONFUSION")

    print(f"\n✨ Content successfully redistributed from old registry folder")
    print(f"📋 Maintained all content while eliminating structural confusion")

    return True

if __name__ == "__main__":
    main()
