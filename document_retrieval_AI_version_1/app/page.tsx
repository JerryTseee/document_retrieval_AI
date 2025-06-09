"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Upload, FileText, Search, Download, CheckCircle, AlertCircle, FolderOpen, Copy, Trash2 } from "lucide-react"

interface DocumentMatch {
  type: string
  files: string[]
}

interface ProcessingResult {
  requiredDocs: string[]
  matches: DocumentMatch[]
  totalCopied: number
}

export default function PDFDocumentMatcher() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [searchFolders, setSearchFolders] = useState("database")
  const [outputFolder, setOutputFolder] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<ProcessingResult | null>(null)
  const [currentStep, setCurrentStep] = useState("")

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && file.type === "application/pdf") {
      setSelectedFile(file)
      setOutputFolder(file.name.replace(".pdf", "") + "_output")
    }
  }

  const simulateProcessing = async () => {
    setIsProcessing(true)
    setProgress(0)
    setCurrentStep("Reading PDF content...")

    // Simulate PDF reading
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setProgress(25)

    setCurrentStep("Identifying required documents...")
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setProgress(50)

    setCurrentStep("Searching for matching files...")
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setProgress(75)

    setCurrentStep("Copying matching documents...")
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setProgress(100)

    // Simulate results
    const mockResults: ProcessingResult = {
      requiredDocs: [
        "certificate",
        "audit report",
        "license",
        "registration",
        "contract",
        "datasheet",
        "profile",
        "experience",
      ],
      matches: [
        {
          type: "certificate",
          files: ["ISO_9001_Certificate.pdf", "Quality_Certificate.pdf"],
        },
        {
          type: "audit report",
          files: ["Annual_Audit_Report_2023.pdf"],
        },
        {
          type: "license",
          files: ["Business_License.pdf", "Operating_License.pdf"],
        },
        {
          type: "registration",
          files: ["Company_Registration.pdf"],
        },
        {
          type: "datasheet",
          files: ["Product_Datasheet_A.pdf", "Technical_Datasheet.pdf", "Spec_Sheet.pdf"],
        },
      ],
      totalCopied: 9,
    }

    setResults(mockResults)
    setIsProcessing(false)
    setCurrentStep("Processing complete!")
  }

  const handleProcess = () => {
    if (!selectedFile) return
    simulateProcessing()
  }

  const handleReset = () => {
    setSelectedFile(null)
    setResults(null)
    setProgress(0)
    setCurrentStep("")
    setOutputFolder("")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900">PDF Document Matcher</h1>
          <p className="text-lg text-gray-600">
            Automatically find and organize required documents from your PDF specifications
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className="space-y-6">
            {/* File Upload */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  Upload PDF Document
                </CardTitle>
                <CardDescription>Select the PDF that contains document requirements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                    <input type="file" accept=".pdf" onChange={handleFileSelect} className="hidden" id="pdf-upload" />
                    <label htmlFor="pdf-upload" className="cursor-pointer">
                      <FileText className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                      {selectedFile ? (
                        <div>
                          <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                          <p className="text-xs text-gray-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                      ) : (
                        <div>
                          <p className="text-sm font-medium text-gray-900">Click to upload PDF</p>
                          <p className="text-xs text-gray-500">or drag and drop</p>
                        </div>
                      )}
                    </label>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FolderOpen className="w-5 h-5" />
                  Configuration
                </CardTitle>
                <CardDescription>Set up search parameters and output location</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="search-folders">Search Folders</Label>
                  <Input
                    id="search-folders"
                    value={searchFolders}
                    onChange={(e) => setSearchFolders(e.target.value)}
                    placeholder="database, documents, files"
                  />
                  <p className="text-xs text-gray-500 mt-1">Comma-separated list of folders to search</p>
                </div>
                <div>
                  <Label htmlFor="output-folder">Output Folder</Label>
                  <Input
                    id="output-folder"
                    value={outputFolder}
                    onChange={(e) => setOutputFolder(e.target.value)}
                    placeholder="output_folder"
                  />
                </div>
                <Button onClick={handleProcess} disabled={!selectedFile || isProcessing} className="w-full" size="lg">
                  {isProcessing ? (
                    <>
                      <Search className="w-4 h-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4 mr-2" />
                      Start Processing
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {/* Progress */}
            {isProcessing && (
              <Card>
                <CardHeader>
                  <CardTitle>Processing Progress</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Progress value={progress} className="w-full" />
                  <p className="text-sm text-gray-600">{currentStep}</p>
                </CardContent>
              </Card>
            )}

            {/* Results */}
            {results && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    Processing Results
                  </CardTitle>
                  <CardDescription>Found {results.totalCopied} matching documents</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Summary */}
                  <div className="grid grid-cols-2 gap-4 p-4 bg-green-50 rounded-lg">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{results.requiredDocs.length}</div>
                      <div className="text-sm text-green-700">Document Types Found</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{results.totalCopied}</div>
                      <div className="text-sm text-green-700">Files Copied</div>
                    </div>
                  </div>

                  <Separator />

                  {/* Required Documents */}
                  <div>
                    <h4 className="font-medium mb-2">Required Document Types:</h4>
                    <div className="flex flex-wrap gap-2">
                      {results.requiredDocs.map((doc, index) => (
                        <Badge key={index} variant="secondary">
                          {doc}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <Separator />

                  {/* Matching Files */}
                  <div>
                    <h4 className="font-medium mb-2">Matching Files:</h4>
                    <ScrollArea className="h-64">
                      <div className="space-y-3">
                        {results.matches.map((match, index) => (
                          <div key={index} className="border rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <Badge variant="outline">{match.type}</Badge>
                              <span className="text-xs text-gray-500">{match.files.length} file(s)</span>
                            </div>
                            <div className="space-y-1">
                              {match.files.map((file, fileIndex) => (
                                <div key={fileIndex} className="flex items-center gap-2 text-sm">
                                  <FileText className="w-4 h-4 text-gray-400" />
                                  <span className="flex-1 truncate">{file}</span>
                                  <Button size="sm" variant="ghost" className="h-6 w-6 p-0">
                                    <Copy className="w-3 h-3" />
                                  </Button>
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-4">
                    <Button className="flex-1">
                      <Download className="w-4 h-4 mr-2" />
                      Download Results
                    </Button>
                    <Button variant="outline" onClick={handleReset}>
                      <Trash2 className="w-4 h-4 mr-2" />
                      Reset
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Help Card */}
            {!results && !isProcessing && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 text-blue-500" />
                    How it works
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm text-gray-600">
                  <div className="flex gap-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                      1
                    </div>
                    <p>Upload a PDF containing document requirements</p>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                      2
                    </div>
                    <p>The system extracts and identifies required document types</p>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                      3
                    </div>
                    <p>Searches your specified folders for matching documents</p>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                      4
                    </div>
                    <p>Copies all matching files to your output folder</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
