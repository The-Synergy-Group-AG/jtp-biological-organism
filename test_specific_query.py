#!/usr/bin/env python3
"""Test biological AI discoverability for specific user query: CV customization with gamification"""

import yaml
import os
from pathlib import Path

class BiologicalAISearchTest:
    def __init__(self, docs_root="docs"):
        self.docs_root = Path(docs_root)
        self.documents = {}
        self.keyword_index = {}
        self.load_documents()

    def load_documents(self):
        for root, dirs, files in os.walk(self.docs_root):
            for file in files:
                if file.endswith('.md') and not file.endswith('.bak'):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if not content.startswith('---'):
                            continue

                        parts = content.split('---', 2)
                        if len(parts) < 3:
                            continue

                        metadata = yaml.safe_load(parts[1])
                        if not metadata or 'ai_keywords' not in metadata:
                            continue

                        doc_id = str(filepath.relative_to(self.docs_root))
                        keywords = [k.strip().lower() for k in metadata['ai_keywords'].split(',')]

                        self.documents[doc_id] = {
                            'title': metadata.get('title', doc_id),
                            'keywords': keywords,
                            'ai_summary': metadata.get('ai_summary', ''),
                            'phase': metadata.get('evolutionary_phase', 'unknown'),
                            'biological_system': metadata.get('biological_system', 'unknown')
                        }

                        # Build inverted index
                        for keyword in keywords:
                            if keyword not in self.keyword_index:
                                self.keyword_index[keyword] = []
                            self.keyword_index[keyword].append(doc_id)

                    except Exception as e:
                        pass

    def search_biological_intelligence(self, user_query):
        """Search using biological AI discoverability intelligence"""
        query_terms = [term.lower().strip() for term in user_query.split()]

        print(f"🔍 USER QUERY: '{user_query}'")
        print(f"📝 Extracted Keywords: {query_terms}")
        print()

        # Direct keyword matching
        direct_matches = set()
        related_matches = set()

        for term in query_terms:
            # Exact matches
            if term in self.keyword_index:
                direct_matches.update(self.keyword_index[term])
                print(f"✅ Direct match for '{term}': {len(self.keyword_index[term])} documents")

            # Fuzzy/partial matches (biological intelligence)
            for keyword in self.keyword_index:
                if term in keyword or keyword in term:
                    if '.'.join(keyword.split('.')[:2]) != keyword[:2]:  # Avoid duplicates
                        related_matches.update(self.keyword_index[keyword])
                        print(f"🔄 Related match for '{term}' ≈ '{keyword}': +{len(self.keyword_index[keyword])} documents")

        all_matches = direct_matches.union(related_matches)

        # Sort by relevance (more keywords matched = higher relevance)
        sorted_results = []
        for doc_id in all_matches:
            doc_data = self.documents[doc_id]
            keyword_overlap = len(set(query_terms).intersection(set(doc_data['keywords'])))
            biological_relevance = self.calculate_biological_relevance(doc_data, query_terms)
            total_score = keyword_overlap * 10 + biological_relevance

            sorted_results.append({
                'doc_id': doc_id,
                'title': doc_data['title'],
                'score': total_score,
                'matching_keywords': list(set(query_terms).intersection(set(doc_data['keywords']))),
                'biological_system': doc_data['biological_system'],
                'phase': doc_data['phase'],
                'ai_summary': doc_data['ai_summary']
            })

        sorted_results.sort(key=lambda x: x['score'], reverse=True)

        print("\n📊 BIOLOGICAL AI SEARCH RESULTS:")
        print(f"   • Total documents analyzed: {len(self.documents)}")
        print(f"   • Direct keyword matches: {len(direct_matches)}")
        print(f"   • Extended biological connections: {len(related_matches)}")
        print(f"   • Total relevant documents found: {len(sorted_results)}")
        print()

        if sorted_results:
            print("🏆 MOST RELEVANT DISCOVERIES:")
            print("=" * 80)
            for i, result in enumerate(sorted_results[:10], 1):
                print(f"{i}. 📄 {result['title']}")
                print(f"   🎯 Biological AI Relevance Score: {result['score']}/100")
                print(f"   🏗️  Evolutionary Phase: {result['phase']}")
                print(f"   🧬 Biological System: {result['biological_system']}")
                if result['matching_keywords']:
                    print(f"   🔑 Direct keyword matches: {', '.join(result['matching_keywords'])}")
                if result['ai_summary']:
                    summary = result['ai_summary'][:120] + "..." if len(result['ai_summary']) > 120 else result['ai_summary']
                    print(f"   🧠 Content Summary: {summary}")
                print()
        else:
            print("❌ NO DOCUMENTS FOUND - Biological AI discoverability returning empty results")
            print("💡 This means the query concepts are not present in the current documentation")
            print("📝 To add this knowledge, we would need to create documentation with appropriate biological keywords")

        return sorted_results

    def calculate_biological_relevance(self, doc_data, query_terms):
        """Calculate biological intelligence relevance score"""
        score = 0

        # Biological system relevance
        biological_keywords = ['biological', 'consciousness', 'harmonization', 'godhood', 'evolution']
        for bio_term in biological_keywords:
            if bio_term in doc_data['biological_system'].lower() or bio_term in query_terms:
                score += 3

        # Phase relevance (later phases generally more sophisticated)
        try:
            phase_num = float(doc_data['phase'].split('.')[0])
            if phase_num > 10:  # Advanced phases
                score += 2
        except:
            pass

        # Keyword density relevance
        keyword_density = len(doc_data['keywords']) / 12.0 * 10  # Max 10 points for full compliance
        score += min(keyword_density, 10)

        return score

def test_user_cv_gamification_query():
    """Test the specific user query: customizing CV with gamification points"""

    print("🧪 TESTING REAL-WORLD USER QUERY DISCOVERABILITY")
    print("=" * 70)
    print()

    # Initialize biological AI engine
    ai_engine = BiologicalAISearchTest()

    # Test multiple variations of the CV/gamification query
    test_queries = [
        "cv customization gamification points",
        "CV gamification customization",
        "resume gamification",
        "document cv gamification"
    ]

    for query in test_queries:
        print(f"🔍 QUERY TEST: '{query}'")
        print("-" * 50)
        results = ai_engine.search_biological_intelligence(query)
        print()

        if not results:
            print("📝 CONCLUSION: This specific concept needs documentation")
            print()

if __name__ == "__main__":
    test_user_cv_gamification_query()
