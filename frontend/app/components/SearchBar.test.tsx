import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import SearchBar from "./SearchBar";

describe("SearchBar", () => {
  test("onSearch is called only on Enter", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByPlaceholderText(/search by audio filename.../i);

    fireEvent.change(input, { target: { value: "hello" } });
    expect(onSearch).not.toHaveBeenCalled();

    fireEvent.keyDown(input, { key: "Enter" });
    expect(onSearch).toHaveBeenCalledTimes(1);
    expect(onSearch).toHaveBeenCalledWith("hello");

    fireEvent.change(input, { target: { value: "world" } });
    fireEvent.keyDown(input, { key: "Shift" });
    expect(onSearch).toHaveBeenCalledTimes(1); // still 1, not 2
    expect(onSearch).not.toHaveBeenCalledWith("world");
  });
});
